"""Keeps Hyperion's LED output switched on.

Hyperion 2.2.1 disables its LEDDEVICE component whenever the WLED node
reboots or is switched off mid-stream (a cfg write, a Night preset, a power
cut), and never re-enables it. This loop asks every 20 s and turns it back
on. Runs at login from a Startup shortcut (pythonw, no window).

Token: an API token created in Hyperion, stored next to this file in
hyperion_token.txt (git-ignored).
"""
import json, pathlib, time, urllib.request

URL = "http://localhost:8090/json-rpc"
TOKEN = (pathlib.Path(__file__).with_name("hyperion_token.txt")).read_text().strip()


def rpc(d):
    r = urllib.request.Request(URL, data=json.dumps(d).encode(),
                               headers={"Content-Type": "application/json", "Authorization": "token " + TOKEN})
    return json.load(urllib.request.urlopen(r, timeout=5))


def once():
    info = rpc({"command": "serverinfo", "tan": 1}).get("info", {})
    comps = {c["name"]: c["enabled"] for c in info.get("components", [])}
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
