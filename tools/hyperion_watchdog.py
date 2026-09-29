"""Room supervisor: keeps screen sync and Home Assistant running, unattended.

Started by the Windows scheduled task "RoomSupervisor" (at logon, on unlock,
on resume from sleep/hibernate; restarted by Task Scheduler if it dies) and,
as a fallback, by the HKCU Run key. Only one copy runs: a second copy exits
at once (it cannot bind the lock port).

Every 20 s it makes sure that:
  * hyperiond.exe is running (starts it if not);
  * WSL Ubuntu is up - one `sleep infinity` held open so the distro, systemd,
    dockerd and the unless-stopped Home Assistant + Whisper containers stay
    up - and Home Assistant answers on localhost:8123; if it has not answered
    for 3 minutes, runs `docker compose up -d` inside Ubuntu;
  * Hyperion captures the 2560-wide Dell (its DDA input index moves with the
    laptop lid), its grabber is not idle, and its LED output is enabled
    (Hyperion 2.2.1 switches LED output off whenever the WLED node reboots).

Everything it does, and every error with a traceback, goes to
tools/logs/room_supervisor.log (rotating, 3 x 1 MB).

Token: a Hyperion API token in hyperion_token.txt next to this file (git-ignored).
"""
import json, logging, logging.handlers, pathlib, socket, subprocess, sys, time, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
HYPERIOND = pathlib.Path("D:/games/Hyperion/bin/hyperiond.exe")
HYPERION_RPC = "http://localhost:8090/json-rpc"
HA_URL = "http://localhost:8123/"
TOKEN = (HERE / "hyperion_token.txt").read_text().strip()
LOCK_PORT = 47831
NO_WINDOW = 0x08000000          # CREATE_NO_WINDOW
DETACHED = 0x00000008           # DETACHED_PROCESS
QUIET = dict(stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

(HERE / "logs").mkdir(exist_ok=True)
log = logging.getLogger("room")
log.setLevel(logging.INFO)
_h = logging.handlers.RotatingFileHandler(HERE / "logs" / "room_supervisor.log", maxBytes=1_000_000, backupCount=3,
                                          encoding="utf-8")
_h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
log.addHandler(_h)


def rpc(d):
    r = urllib.request.Request(HYPERION_RPC, data=json.dumps(d).encode(),
                               headers={"Content-Type": "application/json", "Authorization": "token " + TOKEN})
    return json.load(urllib.request.urlopen(r, timeout=5))


def run_quiet(args, timeout=30):
    return subprocess.run(args, capture_output=True, text=True, creationflags=NO_WINDOW, timeout=timeout)


# ---------------------------------------------------------------- Hyperion
def hyperion_running():
    return "hyperiond.exe" in run_quiet(["tasklist", "/FI", "IMAGENAME eq hyperiond.exe"]).stdout


def ensure_hyperiond():
    if hyperion_running():
        return False
    subprocess.Popen([str(HYPERIOND)], cwd=str(HYPERIOND.parent), creationflags=DETACHED | NO_WINDOW, **QUIET)
    log.info("started hyperiond")
    return True


LAST_SCREEN_CHECK = 0.0


def pick_dell_screen():
    """Point the DDA grabber at whichever input is 2560 wide (the Dell)."""
    d = rpc({"command": "inputsource", "subcommand": "discover", "sourceType": "screen", "tan": 5})
    dda = [v for v in d.get("info", {}).get("video_sources", []) if v.get("device") == "dda"]
    if not dda:
        return
    want = None
    for vi in dda[0].get("video_inputs", []):
        if vi["formats"][0]["resolutions"][0].get("width") == 2560:
            want = vi["inputIdx"]
    if want is None:
        return
    fg = rpc({"command": "config", "subcommand": "getconfig", "tan": 6})["info"]["global"]["settings"]["framegrabber"]
    if fg.get("input") == want and fg.get("width") == 2560:
        return
    fg.update({"input": want, "width": 2560, "height": 1440, "device": "dda", "enable": True})
    rpc({"command": "config", "subcommand": "setconfig", "config": {"global": {"settings": {"framegrabber": fg}}}, "tan": 7})
    log.info("grabber moved to input %d", want)


def tend_hyperion():
    global LAST_SCREEN_CHECK
    if ensure_hyperiond():
        return                                  # give it a cycle to come up
    if time.time() - LAST_SCREEN_CHECK > 60:
        LAST_SCREEN_CHECK = time.time()
        pick_dell_screen()
    info = rpc({"command": "serverinfo", "tan": 1}).get("info", {})
    comps = {c["name"]: c["enabled"] for c in info.get("components", [])}
    grab = [x for x in info.get("priorities", []) if x.get("componentId") == "GRABBER"]
    if comps.get("GRABBER") and grab and not grab[0].get("active"):
        rpc({"command": "componentstate", "componentstate": {"component": "GRABBER", "state": False}, "tan": 3})
        time.sleep(2)
        rpc({"command": "componentstate", "componentstate": {"component": "GRABBER", "state": True}, "tan": 4})
        log.info("restarted idle GRABBER")
    if comps.get("LEDDEVICE") is False:
        rpc({"command": "componentstate", "componentstate": {"component": "LEDDEVICE", "state": True}, "tan": 2})
        log.info("re-enabled LEDDEVICE")


# ------------------------------------------------------ WSL + Home Assistant
KEEPER = None
HA_DOWN_SINCE = None
LAST_COMPOSE = 0.0


def ha_up():
    try:
        urllib.request.urlopen(HA_URL, timeout=4)
        return True
    except Exception:
        return False


def tend_home_assistant():
    global KEEPER, HA_DOWN_SINCE, LAST_COMPOSE
    if KEEPER is None or KEEPER.poll() is not None:
        KEEPER = subprocess.Popen(["wsl.exe", "-d", "Ubuntu", "-u", "root", "-e", "sleep", "infinity"],
                                  creationflags=NO_WINDOW, **QUIET)
        log.info("started WSL keeper (pid %d)", KEEPER.pid)
    if ha_up():
        if HA_DOWN_SINCE is not None:
            log.info("Home Assistant is up (was down %.0f s)", time.time() - HA_DOWN_SINCE)
        HA_DOWN_SINCE = None
        return
    now = time.time()
    if HA_DOWN_SINCE is None:
        HA_DOWN_SINCE = now
        log.info("Home Assistant not answering yet")
    if now - HA_DOWN_SINCE > 180 and now - LAST_COMPOSE > 300:
        LAST_COMPOSE = now
        r = run_quiet(["wsl.exe", "-d", "Ubuntu", "-u", "root", "-e", "docker", "compose", "-f",
                       "/opt/homeassistant/docker-compose.yml", "up", "-d"], timeout=600)
        log.warning("HA down for %.0f s - ran compose up: rc=%s %s", now - HA_DOWN_SINCE, r.returncode,
                    (r.stdout + r.stderr).strip()[-300:])


# ------------------------------------------------------------------- main
def main():
    lock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        lock.bind(("127.0.0.1", LOCK_PORT))
    except OSError:
        log.info("another supervisor is already running - exiting")
        return
    lock.listen(1)
    log.info("supervisor started (pid-less pythonw), python %s", sys.version.split()[0])
    while True:
        for step in (tend_home_assistant, tend_hyperion):
            try:
                step()
            except Exception:
                log.exception("%s failed", step.__name__)
        time.sleep(20)


if __name__ == "__main__":
    if "--once" in sys.argv:
        log.addHandler(logging.StreamHandler(sys.stdout))
        tend_home_assistant(); tend_hyperion()
        print("HA up:", ha_up(), "| hyperiond running:", hyperion_running())
        sys.exit()
    try:
        main()
    except BaseException:
        log.exception("supervisor crashed")
        raise
