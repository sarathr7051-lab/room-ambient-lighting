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

## Lighting tags, final form (Home Assistant)

Once the HA Companion app is on the phone, the lighting tags carry HA tag
URLs instead of WLED URLs, so one tap also sets the bulb:

| Tag | URL record |
|---|---|
| Work | `https://www.home-assistant.io/tag/room-work` |
| Evening | `https://www.home-assistant.io/tag/room-evening` |
| Screen sync | `https://www.home-assistant.io/tag/room-screen-sync` |
| (Movie, Night - no tag yet) | `https://www.home-assistant.io/tag/room-movie`, `.../room-night` |

The WLED URLs above still work as a fallback if HA is down.

## Artist tags

Artist IDs come from the Spotify app: artist page -> share -> copy link ->
the 22-character string after `/artist/`. Searching by name is not reliable -
"Pradeep Kumar" returns a dozen artists.

| Card | Artist | Spotify ID (verified on open.spotify.com, 27 Sep) | Record to write |
|---|---|---|---|
| Rahman | A. R. Rahman | `1mYsTxnqsietFxj1OgoGbG` | `spotify:artist:1mYsTxnqsietFxj1OgoGbG:play` |
| MJ | Michael Jackson | `3fMbdgg4jU18AjLCKBhRSm` | `spotify:artist:3fMbdgg4jU18AjLCKBhRSm:play` |
| Pradeep Kumar | Pradeep Kumar (Tamil; Nee Kavithaigala, 7M monthly) | `15ClyGUe5g2vllncIC4tp6` | `spotify:artist:15ClyGUe5g2vllncIC4tp6:play` |
| Coldplay | Coldplay | `4gzpq5DPGxSnKTe4SA8HAU` | `spotify:artist:4gzpq5DPGxSnKTe4SA8HAU:play` |
| Freddie | Queen | `1dfeR4HaWDbWqFHLkxsg1d` | `spotify:artist:1dfeR4HaWDbWqFHLkxsg1d:play` |
| Anirudh | Anirudh Ravichander | `4zCH9qm4R2DADamUHMCa6O` | `spotify:artist:4zCH9qm4R2DADamUHMCa6O:play` |
| Karan Aujla | Karan Aujla | `6DARBhWbfcS9E4yJzcliqQ` | `spotify:artist:6DARBhWbfcS9E4yJzcliqQ:play` |

**The pack of 10 (decided 27 Sep):** all seven musicians get a tag, plus three
lighting tags - **Screen sync**, **Work**, **Evening**. Movie and Night are
phone taps (bookmarks) until a second pack; the bedside sleep tag too.

### Why a plain Spotify link on the tag does not work (tested 27 Sep)

Both `spotify:artist:<id>:play` and `https://open.spotify.com/artist/<id>`
written directly to a tag open Spotify at its home page and play nothing.
That is a long-known Spotify bug: its NFC (NDEF) handler ignores the path
([shkspr.mobi, 2020](https://shkspr.mobi/blog/2020/09/how-can-i-launch-a-spotify-album-from-an-nfc-tag/),
Spotify engineers acknowledged it). The same links work when another app
opens them normally. So the tag must point at an intermediary app, which then
tells Spotify what to play.

### The zero-tap method that WORKS (27 Sep 2026): Samsung Modes and Routines

No extra app. Settings -> Modes and Routines -> **Routines** -> + ->
**If** -> *NFC tagged* (under Connections; hold the phone on the tag to
register it) -> **Then** -> search **Spotify** -> **Play playlist** -> pick
the official **"This Is <artist>"** playlist (save it to your library in
Spotify first so it appears) -> Save. Tap the tag with the phone unlocked:
Spotify starts playing. Tested with Rahman.

Notes: the routine keys on the tag's ID, so the tag should be **blank** (NFC
Tools -> Other -> Erase) or the phone will also open whatever URL is on it.
Shuffle is Spotify's own setting. The Spotify integration in Routines has
been known to go quiet after a Spotify update; recreating the routine with
Spotify open fixed it for others.

### Fallback: HTTP Shortcuts + a "play from search" intent

**HTTP Shortcuts** (free, open source, already in the handover plan for the
lighting tags) can run a tiny script when opened by a deep link, and the deep
link can live on the tag. The script sends Android's standard
`MEDIA_PLAY_FROM_SEARCH` intent to Spotify - the same request the Google
Assistant uses for "play X on Spotify" - which starts playback with no tap.

One shortcut per artist, type **Scripting**, with this in the script box
(change the two names):

```javascript
sendIntent({
  type: 'activity',
  action: 'android.media.action.MEDIA_PLAY_FROM_SEARCH',
  packageName: 'com.spotify.music',
  newTask: true,
  extras: [
    { name: 'query', type: 'string', value: 'A. R. Rahman' },
    { name: 'android.intent.extra.focus', type: 'string', value: 'vnd.android.cursor.item/artist' },
    { name: 'android.intent.extra.artist', type: 'string', value: 'A. R. Rahman' }
  ]
});
```

Then long-press the shortcut -> **Show Info** -> copy its **deep-linking URL**
(`http-shortcuts://...`) -> that URL is what NFC Tools writes to the tag
(URL / URI record). Tap the tag: HTTP Shortcuts opens for a moment, Spotify
starts the artist. Shuffle is Spotify's own setting.

**Fallback if the search intent only opens Spotify without playing** (Spotify
has broken and unbroken this over the years): replace the script with the
"browse" form, which the Tasker community found still autoplays where the
search intent does not
([Spotify community, 2019](https://community.spotify.com/t5/Android/Tasker-cannot-start-a-Playlist-anymore-Send-intent-does-not-wrok/td-p/4633926)):

```javascript
sendIntent({ type: 'activity', action: 'android.intent.action.VIEW',
             dataUri: 'spotify:artist:1mYsTxnqsietFxj1OgoGbG:play',
             packageName: 'com.spotify.music', newTask: true });
```

Test on **one** artist with the tag held loose before writing the other six.
Screen must be unlocked either way - Android does not read tags on the lock
screen.

Sources: [Spotify community - NFC Tools or Tasker](https://community.spotify.com/t5/Android/NFC-Tools-or-Tasker/td-p/1555062),
[HTTP Shortcuts scripting - sendIntent](https://http-shortcuts.rmy.ch/scripting),
[HTTP Shortcuts FAQ - deep links and NFC](https://http-shortcuts.rmy.ch/faq).

## Writing a tag (NFC Tools)

1. Write -> Add a record -> **URL/URI** -> paste the URL or URI -> OK.
2. Write / <n> bytes -> hold the phone on the tag until it says done.
3. Tap it once to test before it goes on the card.
4. Optional: Other -> Lock tag, so nothing overwrites it. Only after testing.
