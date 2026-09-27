# NFC tags: tap a poster, get a mood or an artist

Tags are NTAG213/215 stickers on the **back** of five poster cards (centred,
1 cm from any edge, 3 cm from any other tag, never on metal). Written once
with the **NFC Tools** app (Android) as a single record. Nothing on the phone
has to be running: Android reads a URL record and opens it.

## Two kinds of record

| Tap | Record written to the tag | What happens |
|---|---|---|
| Lighting mood | URL, e.g. `http://192.168.1.6/win&PL=2&LO=2` | the desk node loads preset 2 and overrides the screen sync; the shelf node follows over UDP |
| Screen sync back on | URL `http://192.168.1.6/win&PL=6&LO=0` | hands the strip back to Hyperion |
| Artist | URI `spotify:artist:<id>:play` | Spotify opens the artist and starts playing. Shuffle is a Spotify setting: turn it on once in the app and it stays on |

The mood URLs need the desk node's address. It is `192.168.1.6` today but
there is no DHCP reservation; if it ever moves, the tags are rewritten (NFC
Tools -> Write, same 30 seconds). `wled-desk.local` does not work from Android
for this, so the IP it is.

| Slot | Preset | Tag URL |
|---|---|---|
| Work | 1 | `http://192.168.1.6/win&PL=1&LO=2` |
| Evening | 2 | `http://192.168.1.6/win&PL=2&LO=2` |
| Movie | 3 | `http://192.168.1.6/win&PL=3&LO=2` |
| Night (off) | 5 | `http://192.168.1.6/win&PL=5&LO=2` |
| Screen sync | 6 | `http://192.168.1.6/win&PL=6&LO=0` |

`LO=2` = "live override until reboot": the mood wins over Hyperion's stream.
`LO=0` releases it. Without `LO`, a preset call while Hyperion streams does
nothing visible - that is why the plain preset URLs did not work.

## Artist tags

Artist IDs come from the Spotify app: artist page -> share -> copy link ->
the 22-character string after `/artist/`. Searching by name is not reliable -
"Pradeep Kumar" returns a dozen artists.

| Poster | Artist | ID | Record |
|---|---|---|---|
| | A. R. Rahman | _to fill_ | `spotify:artist:<id>:play` |
| | Michael Jackson | _to fill_ | |
| | Pradeep Kumar | _to fill_ | |
| | Coldplay | _to fill_ | |
| | Queen / Freddie Mercury | _to fill_ | |

The `:play` suffix is the old Spotify URI form that still autoplays on
Android; if a phone update breaks it, the fallback is the plain
`https://open.spotify.com/artist/<id>` link (opens the page, one more tap to
play).

## Writing a tag (NFC Tools)

1. Write -> Add a record -> **URL/URI** -> paste the URL or URI -> OK.
2. Write / <n> bytes -> hold the phone on the tag until it says done.
3. Tap it once to test before it goes on the card.
4. Optional: Other -> Lock tag, so nothing overwrites it. Only after testing.
