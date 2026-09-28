"""Keeps Hyperion (and the WSL Ubuntu that hosts Home Assistant) running.

Hyperion 2.2.1 disables its LEDDEVICE component whenever the WLED node
reboots or is switched off mid-stream (a cfg write, a Night preset, a power
cut), and never re-enables it. This loop asks every 20 s and turns it back
on. Runs at login from a Startup shortcut (pythonw, no window).

Token: an API token created in Hyperion, stored next to this file in
hyperion_token.txt (git-ignored).
"""
import json, pathlib, subprocess, time, urllib.request

HYPERIOND = "D:/games/Hyperion/bin/hyperiond.exe"

URL = "http://localhost:8090/json-rpc"
TOKEN = (pathlib.Path(__file__).with_name("hyperion_token.txt")).read_text().strip()


def rpc(d):
    r = urllib.request.Request(URL, data=json.dumps(d).encode(),
                               headers={"Content-Type": "application/json", "Authorization": "token " + TOKEN})
    return json.load(urllib.request.urlopen(r, timeout=5))


def hyperion_running():
    # CREATE_NO_WINDOW: without it every check flashes a console window
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq hyperiond.exe"], capture_output=True, text=True,
                         creationflags=0x08000000).stdout
    return "hyperiond.exe" in out


KEEPER = None


def keep_wsl_alive():
    """Home Assistant runs in Docker inside WSL Ubuntu. WSL stops an idle
    distro, so hold one sleeping process open in it; systemd then keeps
    dockerd - and the unless-stopped containers - running."""
    global KEEPER
    if KEEPER is None or KEEPER.poll() is not None:
        KEEPER = subprocess.Popen(["wsl.exe", "-d", "Ubuntu", "-u", "root", "-e", "sleep", "infinity"],
                                  creationflags=0x08000000, stdin=subprocess.DEVNULL,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "started WSL keeper"
    return None


LAST_SCREEN_CHECK = 0.0


def pick_dell_screen():
    """The DDA input index of the 2560-wide Dell moves: 0 with the laptop lid
    closed, 1 with it open. Point Hyperion at whichever input is 2560 wide."""
    d = rpc({"command": "inputsource", "subcommand": "discover", "sourceType": "screen", "tan": 5})
    dda = [v for v in d.get("info", {}).get("video_sources", []) if v.get("device") == "dda"]
    if not dda:
        return None
    want = None
    for vi in dda[0].get("video_inputs", []):
        res = vi["formats"][0]["resolutions"][0]
        if res.get("width") == 2560:
            want = vi["inputIdx"]
    if want is None:
        return None
    cfg = rpc({"command": "config", "subcommand": "getconfig", "tan": 6})["info"]
    fg = cfg["global"]["settings"]["framegrabber"]
    if fg.get("input") == want and fg.get("width") == 2560:
        return None
    fg.update({"input": want, "width": 2560, "height": 1440, "device": "dda", "enable": True})
    rpc({"command": "config", "subcommand": "setconfig", "config": {"global": {"settings": {"framegrabber": fg}}}, "tan": 7})
    return "grabber moved to input %d" % want


def once():
    global LAST_SCREEN_CHECK
    if not hyperion_running():
        subprocess.Popen([HYPERIOND], creationflags=0x00000008)   # DETACHED_PROCESS
        return "started hyperiond"
    if time.time() - LAST_SCREEN_CHECK > 60:
        LAST_SCREEN_CHECK = time.time()
        moved = pick_dell_screen()
        if moved:
            return moved
    info = rpc({"command": "serverinfo", "tan": 1}).get("info", {})
    comps = {c["name"]: c["enabled"] for c in info.get("components", [])}
    grab = [x for x in info.get("priorities", []) if x.get("componentId") == "GRABBER"]
    if comps.get("GRABBER") and grab and not grab[0].get("active"):
        # after a reboot or a display change the DDA grabber can sit idle
        # with no frames; switching it off and on re-attaches it
        rpc({"command": "componentstate", "componentstate": {"component": "GRABBER", "state": False}, "tan": 3})
        time.sleep(2)
        rpc({"command": "componentstate", "componentstate": {"component": "GRABBER", "state": True}, "tan": 4})
        return "restarted GRABBER"
    if comps.get("LEDDEVICE") is False:
        rpc({"command": "componentstate", "componentstate": {"component": "LEDDEVICE", "state": True}, "tan": 2})
        return "re-enabled LEDDEVICE"
    return "ok"


if __name__ == "__main__":
    import sys
    if "--once" in sys.argv:
        print(once()); sys.exit()
    while True:
        try:
            keep_wsl_alive()
        except Exception:
            pass
        try:
            once()
        except Exception:
            pass
        time.sleep(20)
