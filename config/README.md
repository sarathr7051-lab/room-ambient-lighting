# config/

Generated files, committed so the node can be rebuilt from scratch without
re-deriving anything.

| File | Produced by | Consumed by |
|---|---|---|
| `wled_desk_cfg.json` | `tools/led_layout.py --write` | `tools/wled_push.py apply` |
| `hyperion_leds.json` | `tools/led_layout.py --write` | pasted into Hyperion's LED Layout JSON view |

Both are empty until the monitor strip path is measured. See the "Blocked on"
section of the top-level README.
