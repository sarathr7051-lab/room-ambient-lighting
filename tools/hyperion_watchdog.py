"""Keeps Hyperion's LED output switched on.

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
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq hyperiond.exe"], capture_output=True, text=True).stdout
    return "hyperiond.exe" in out


def once():
    if not hyperion_running():
        subprocess.Popen([HYPERIOND], creationflags=0x00000008)   # DETACHED_PROCESS
        return "started hyperiond"
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
            once()
        except Exception:
            pass
        time.sleep(20)
