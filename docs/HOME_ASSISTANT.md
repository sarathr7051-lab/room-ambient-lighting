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

## Install log

- 27 Sep 2026, evening: Docker Desktop 4.91.0 installed by winget. WSL2
  enabled with admin rights; Windows reports "WSL2 is unable to start since
  virtualization is not enabled" until the PC restarts (the Virtual Machine
  Platform component needs the reboot). If it still says that after the
  restart, Intel VT-x is off in the BIOS - the owner enables it there.
- 27 Sep 2026, after the restart: WSL2 came up (virtualization is on),
  Docker engine 29.8.0, `docker compose up -d` pulled
  `ghcr.io/home-assistant/home-assistant:stable` and **HA answers on
  http://localhost:8123**. Onboarding (owner account) is the owner's step.
- Compose file: `tools/homeassistant/docker-compose.yml`. Config lives in
  `tools/homeassistant/config/` (git-ignored).
- Docker Desktop on Windows has no true host networking, so HA will not
  auto-discover the WLED nodes or Hyperion; they are added by address.

## Built 27 Sep 2026, late evening

| Thing | State |
|---|---|
| WLED desk, WLED shelf | added by IP; entities `light.wled_desk`, `select.wled_desk_preset`, `select.wled_desk_live_override`, `switch.wled_desk_sync_send`, `light.wled_shelf` |
| Hyperion | added at `host.docker.internal:19444`; `light.first_led_hardware_instance` = its LED output (left alone - the watchdog keeps it on) |
| Havells Glamax bulb | via **Tuya** (Smart Life user code + QR, done by the owner); `light.glamax_bulb_tw_rgb`, colour-temp + colour |
| Scripts | `script.mood_work / mood_evening / mood_movie / mood_night / mood_screen_sync` - each: sync-send on, live override 2 (0 for screen sync), desk preset, bulb (Work 80 % 4000 K, Evening 40 % 2700 K, Movie/Night off, Screen sync 15 % 2700 K). Shelf follows the desk over UDP |
| Automations | `Tag: Work / Evening / Movie / Night / Screen sync` - trigger `tag_id` `room-work`, `room-evening`, `room-movie`, `room-night`, `room-screen-sync` -> the script |
| Tag URLs | `https://www.home-assistant.io/tag/room-work` etc. Written to the tags with NFC Tools (URL record); read by the **HA Companion app**, which must be installed and logged in on the phone (server `http://<PC LAN IP>:8123`, 192.168.1.4 on 27 Sep) |

Gotcha found while testing: WLED's *runtime* sync-send flag (`state.udpn.send`) was
off although the config flag was on, so the shelf did not follow. The
scripts now switch `switch.wled_desk_sync_send` on first.

Config lives in `tools/homeassistant/config/` (git-ignored). Everything above
was created through the REST config API from the logged-in browser session.

## Voice, without Google or Alexa

Google Assistant / Alexa need either the paid Home Assistant Cloud or an
HTTPS route into this network with port forwarding - and this router's admin
page is not reachable, so port forwarding is out. **HA's own Assist** does the
job locally and free: the Companion app can be set as the phone's default
assistant (Android: Settings -> Apps -> Default apps -> Digital assistant app
-> Home Assistant), so the power-button / long-press gesture opens Assist and
the phone's own speech recognition feeds it.

Set up 27 Sep: bulb, desk and shelf lights and the five mood scripts exposed
to Assist; bulb named **"Bedroom light"** (aliases bulb / bedroom bulb);
conversation-trigger automations `Voice: Work / Evening / Movie / Night /
Screen sync` answering to: *work mode, work, work lights / evening mode,
evening / movie mode, movie / night mode, night, lights off, good night /
screen sync, sync, ambilight*. Built-in phrases also work: *set the bedroom
light to green*, *set the bedroom light to 30 percent*, *turn off the desk
light*. Tested by text through the conversation API: all answered "Done" /
"Color set" / "Brightness set".

## Not tonight

Setup order once the host exists: install HA container -> open
http://localhost:8123 -> create the HA owner account (owner does this) ->
integrations auto-discover both WLED nodes and Hyperion -> add Smart Life with
the app account -> build the five scenes -> Companion app.
