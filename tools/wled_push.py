#!/usr/bin/env python3
"""
wled_push.py - drive the desk node over Wi-Fi. No serial port, no COM port,
no flashing. WLED is flashed once by hand from install.wled.me; after that
every change to this project happens over HTTP, which is what this tool does.

Standard library only. No pip install.

    python tools/wled_push.py probe   --host 192.168.1.42
    python tools/wled_push.py walk    --host 192.168.1.42
    python tools/wled_push.py apply   --host 192.168.1.42
    python tools/wled_push.py presets --host 192.168.1.42

`--host` takes an IP or an mDNS name (wled-desk.local).
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent
AMBER = "EF9F27"


# --------------------------------------------------------------------------
# transport
# --------------------------------------------------------------------------

def _url(host: str, path: str) -> str:
    host = host.strip().removeprefix("http://").removeprefix("https://").rstrip("/")
    return f"http://{host}{path}"


def get(host: str, path: str, timeout: float = 5.0):
    req = urllib.request.Request(_url(host, path), method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def post(host: str, path: str, payload: dict, timeout: float = 8.0):
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        _url(host, path), data=body, method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8").strip()
    try:
        return json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        return {"raw": raw}


def die(msg: str) -> None:
    print(f"  ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def reachable(host: str) -> dict:
    try:
        return get(host, "/json/info")
    except urllib.error.URLError as e:
        die(f"cannot reach {host} - {e.reason}\n"
            f"         Is the node powered and on the 2.4 GHz network? "
            f"Try the IP shown in your router's client list.")
    except TimeoutError:
        die(f"timed out talking to {host}")
    return {}


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_probe(a) -> None:
    info = reachable(a.host)
    state = get(a.host, "/json/state")
    leds = info.get("leds", {})

    print(f"\n  {info.get('name', '?')}  @  {a.host}")
    print(f"  {'-' * 56}")
    print(f"  WLED           {info.get('ver', '?')}  (build {info.get('vid', '?')})")
    print(f"  chip           {info.get('arch', '?')}  "
          f"free heap {info.get('freeheap', 0) / 1024:.0f} kB")
    print(f"  wifi           {info.get('wifi', {}).get('signal', '?')}%  "
          f"ch {info.get('wifi', {}).get('channel', '?')}")
    print(f"  uptime         {info.get('uptime', 0)} s")
    print(f"  LED count      {leds.get('count', '?')}")
    print(f"  max power      {leds.get('maxpwr', '?')} mA")
    print(f"  est. current   {leds.get('pwr', '?')} mA  (right now)")
    print(f"  fps            {leds.get('fps', '?')}")
    print(f"  on / bri       {state.get('on')} / {state.get('bri')}")

    ver = str(info.get("ver", ""))
    if ver and not ver.startswith(("0.1", "1.")):
        print(f"\n  note: unexpected version string {ver!r}")
    print("\n  Hyperion needs WLED >= 0.11 for DDP, and >= 0.13.3 if you ever")
    print("  want segment streaming. Anything current is fine.\n")


def cmd_apply(a) -> None:
    """POST the generated LED bus config, then read it back and diff."""
    path = REPO / "config" / "wled_desk_cfg.json"
    if not path.exists():
        die(f"{path.relative_to(REPO)} not found - run led_layout.py --write first")

    want = json.loads(path.read_text(encoding="utf-8"))
    reachable(a.host)

    before = get(a.host, "/json/info").get("leds", {}).get("count")
    print(f"\n  LED count before: {before}")

    post(a.host, "/json/cfg", want)
    time.sleep(1.5)  # WLED re-inits the bus and rewrites cfg.json

    after_info = get(a.host, "/json/info").get("leds", {})
    want_led = want["hw"]["led"]

    ok = True
    checks = [
        ("count", want_led["total"], after_info.get("count")),
        ("maxpwr", want_led["maxpwr"], after_info.get("maxpwr")),
    ]
    print(f"  {'-' * 46}")
    for name, expect, got in checks:
        mark = "ok " if expect == got else "BAD"
        if expect != got:
            ok = False
        print(f"  {mark}  {name:<10} want {expect!s:<8} got {got!s}")

    if ok:
        print("\n  Bus config applied and verified.\n")
    else:
        print("\n  Read-back does not match. /json/cfg is only partially")
        print("  documented and the schema moves between WLED releases.")
        print("  Fallback that always works: open the node's web UI ->")
        print("  Config -> LED Preferences and set it by hand:")
        print(f"    type WS281x  *  GPIO {want_led['ins'][0]['pin'][0]}  *  "
              f"{want_led['total']} LEDs  *  GRB  *  "
              f"ABL {want_led['maxpwr']} mA\n")
        sys.exit(2)


def _blackout(host: str, n: int) -> None:
    post(host, "/json/state",
         {"on": True, "bri": 128, "seg": [{"id": 0, "fx": 0, "i": [0, n, "000000"]}]})


def cmd_walk(a) -> None:
    """
    Chase one white pixel around the frame so you can confirm, with your eyes,
    where LED 0 is and which way the strip runs - before the Hyperion layout
    is built on an assumption.
    """
    info = reachable(a.host)
    n = info.get("leds", {}).get("count") or 0
    if not n:
        die("node reports 0 LEDs - set the LED count first (apply)")

    print(f"\n  {n} LEDs. Watch the monitor back.")
    print("  LED 0 is RED. A WHITE pixel walks from 0 upward.")
    print("  Ctrl-C to stop.\n")

    try:
        _blackout(a.host, n)
        post(a.host, "/json/state", {"seg": [{"id": 0, "i": [0, "FF0000"]}]})
        time.sleep(1.5)

        for i in range(n):
            post(a.host, "/json/state",
                 {"seg": [{"id": 0, "i": [0, n, "000000", 0, "FF0000", i, "FFFFFF"]}]})
            if i % 10 == 0:
                print(f"    LED {i}")
            time.sleep(a.step)
    except KeyboardInterrupt:
        print("\n  stopped")
    finally:
        _blackout(a.host, n)
        print("\n  Now write down, looking at the FRONT of the screen:")
        print("    - which corner LED 0 sat in")
        print("    - which way the white pixel travelled")
        print("  If it does not match led_layout.py's convention, either")
        print("  re-run led_layout.py with a matching --sides/start, or set")
        print("  'rev': true on the bus to flip direction.\n")


def cmd_identify(a) -> None:
    """First LED red, last LED blue, everything else off. Leaves them lit."""
    info = reachable(a.host)
    n = info.get("leds", {}).get("count") or 0
    if not n:
        die("node reports 0 LEDs")
    post(a.host, "/json/state",
         {"on": True, "bri": 160,
          "seg": [{"id": 0, "fx": 0,
                   "i": [0, n, "000000", 0, "FF0000", n - 1, "0000FF"]}]})
    print(f"\n  LED 0 = red, LED {n - 1} = blue. "
          f"Run `off` when you are done looking.\n")


def cmd_off(a) -> None:
    reachable(a.host)
    post(a.host, "/json/state", {"on": False})
    print("\n  off\n")


def _presets() -> list[dict]:
    """
    Presets 1-5 for the desk node.

    Only the bias strip (bus 0) exists at this stage. The warm under-desk strip
    is bus 1 and arrives with the 12 V adapter; its segment is added to these
    presets then, not now.

    Preset 3 (Movie) deliberately leaves the strip dim and solid - Hyperion
    takes the LEDs over via DDP the moment it starts streaming, and hands them
    back to this preset when it stops.
    """
    return [
        {"n": "Work", "on": True, "bri": 102,
         "seg": [{"id": 0, "fx": 0, "col": [[255, 231, 204]]}]},
        {"n": "Evening", "on": True, "bri": 77,
         "seg": [{"id": 0, "fx": 0, "col": [[239, 159, 39]]}]},
        {"n": "Movie", "on": True, "bri": 26,
         "seg": [{"id": 0, "fx": 0, "col": [[255, 200, 140]]}]},
        {"n": "Music", "on": True, "bri": 128,
         "seg": [{"id": 0, "fx": 0, "col": [[239, 159, 39]]}]},
        {"n": "Night", "on": False,
         "seg": [{"id": 0, "fx": 0, "col": [[255, 180, 110]]}]},
    ]


def cmd_presets(a) -> None:
    reachable(a.host)
    print()
    for slot, pre in enumerate(_presets(), start=1):
        payload = dict(pre)
        payload["psave"] = slot
        post(a.host, "/json/state", payload)
        time.sleep(0.4)
        print(f"  preset {slot}  {pre['n']}")
    print("\n  Saved. Recall from anything with:")
    print(f"    http://{a.host}/win&PL=1   (the NFC tags use this form)")
    print("\n  Preset 4 'Music' is a placeholder - real sound reactivity needs")
    print("  a WLED build with USERMOD_AUDIOREACTIVE and the INMP441 wired in.")
    print("  That is a later stage and does NOT block screen sync.\n")


# --------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--host", required=True, help="node IP or mDNS name")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("probe", help="version, LED count, power, wifi").set_defaults(fn=cmd_probe)
    sub.add_parser("apply", help="push config/wled_desk_cfg.json and verify").set_defaults(fn=cmd_apply)
    sub.add_parser("identify", help="light first and last LED").set_defaults(fn=cmd_identify)
    sub.add_parser("presets", help="save presets 1-5").set_defaults(fn=cmd_presets)
    sub.add_parser("off", help="turn the strip off").set_defaults(fn=cmd_off)

    w = sub.add_parser("walk", help="chase a pixel to verify strip orientation")
    w.add_argument("--step", type=float, default=0.12, help="seconds per LED")
    w.set_defaults(fn=cmd_walk)

    a = p.parse_args()
    a.fn(a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
