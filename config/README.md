# config/

Generated files, committed so the node can be rebuilt from scratch without
re-deriving anything. **Both are populated.**

| File | Produced by | Consumed by |
|---|---|---|
| `wled_desk_cfg.json` | `tools/led_layout.py --write` | `tools/wled_push.py apply` |
| `hyperion_leds.json` | `tools/led_layout.py --write` | pasted into Hyperion's LED Layout JSON view |

Regenerated 26 Sep 2026 from a measured strip path of **57 x 30.5 cm**:
**70 LEDs**, 18 left / 34 top / 18 right, GPIO16, GRB, skip 0, **ABL 800 mA while the node is on the breadboard**
(regenerate with `--abl 2000` once it moves to a dot board).

Regenerate with:

```bash
python tools/led_layout.py --width 57 --height 30.5 --write
```

Neither file has been pushed to the node yet - it carries a 120-LED bench
config with six colour bands for testing the uncut strip. See [../docs/PROJECT_STATE.md](../docs/PROJECT_STATE.md).
