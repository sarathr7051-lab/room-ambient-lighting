# Home Assistant - one phone app for all of it

Goal: one screen on the phone with the four moods, each setting the desk
strip, the shelf strip **and the Havells bulb** together, plus Hyperion on/off.
WLED nodes and Hyperion have their own web pages already; the bulb is the
part that needs a hub, and Home Assistant (HA) is the hub.

## Where HA runs

HA needs an always-on computer. Options, cheapest first:

| Host | Cost | Catch |
|---|---|---|
| **Docker Desktop on this PC** | free | only works while the PC is on - which is when the room is in use anyway. Docker Desktop is not installed yet (checked 27 Sep); it needs WSL2 and a ~500 MB download |
| Raspberry Pi 4/5 + SD card | a purchase, not priced here | always on, the "proper" way |
| Old Android phone | - | HA does not run on Android |

Decision pending: Docker Desktop on this PC is the plan unless the owner
wants it always-on.

## What plugs into HA

| Thing | HA integration | Needs from the owner |
|---|---|---|
| wled-desk, wled-shelf | **WLED** (auto-discovered) | nothing |
| Hyperion | **Hyperion** (auto-discovered on the same PC) | nothing - gives an on/off switch and the priority list |
| Havells smart bulb | **Tuya** or **Smart Life** (Havells bulbs are Tuya-based) | the bulb must be paired in the **Smart Life** (or Havells) app first, and HA logs in with that app account. The owner creates that account; it cannot be created on his behalf |
| Phone | **HA Companion** app | install, log in once |

## The four moods as HA scenes

| Scene | desk strip | shelf strip | bulb | Hyperion |
|---|---|---|---|---|
| Work | preset 1 | follows | on, cool white, 80 % | off |
| Evening | preset 2 | follows | on, warm, 40 % | off |
| Movie | preset 3 | follows | off | off |
| Night | off | off | off | off |
| Screen sync | preset 6 | - | as before | **on** |

Each scene is one tap in the Companion app, and the NFC tags can point at
HA scenes instead of raw WLED URLs later.

## Not tonight

Setup order once the host exists: install HA container -> open
http://localhost:8123 -> create the HA owner account (owner does this) ->
integrations auto-discover both WLED nodes and Hyperion -> add Smart Life with
the app account -> build the five scenes -> Companion app.
