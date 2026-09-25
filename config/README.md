# config/

Generated files, committed so the node can be rebuilt from scratch without
re-deriving anything. **Both are populated.**

| File | Produced by | Consumed by |
|---|---|---|
| `wled_desk_cfg.json` | `tools/led_layout.py --write` | `tools/wled_push.py apply` |
| `hyperion_leds.json` | `tools/led_layout.py --write` | pasted into Hyperion's LED Layout JSON view |

Generated 25 Sep 2026 from a measured strip path of **57 x 30.5 cm**:
**70 LEDs**, 18 left / 34 top / 18 right, GPIO16, GRB, ABL 3000 mA.

Regenerate with:

```bash
python tools/led_layout.py --width 57 --height 30.5 --write
```

Neither file has been pushed to the node yet - it still reports the WLED
default of 30 LEDs. See [../docs/PROJECT_STATE.md](../docs/PROJECT_STATE.md).
