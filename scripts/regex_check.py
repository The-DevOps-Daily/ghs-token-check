"""Run each pattern in patterns.txt against the live token and report how much of it stays visible."""
import os, re
from patterns import load

t = os.environ["TOKEN"]
print(f"token length {len(t)}")
for name, rx in load():
    m = re.search(rx, t)
    visible = len(t) - (len(m.group(0)) if m else 0)
    print(f"{name:20s} matched={'yes' if m else 'no ':3s} match_len={len(m.group(0)) if m else 0:4d} visible_after_redaction={visible:4d}")
