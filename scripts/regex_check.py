"""Run common token regexes against the token and report how much of it each one leaves visible."""
import os, re

t = os.environ["TOKEN"]
line = f"curl -H 'Authorization: token {t}' https://api.github.com/repos/o/r"
patterns = {
    "legacy docs shape   ghs_[0-9a-zA-Z]{36}": r"ghs_[0-9a-zA-Z]{36}",
    "with underscore     (ghu|ghs)_[A-Za-z0-9_]{36}": r"(ghu|ghs)_[A-Za-z0-9_]{36}",
    "word-bounded        \\bghs_[A-Za-z0-9_]{36}\\b": r"\bghs_[A-Za-z0-9_]{36}\b",
    "open-ended          ghs_[A-Za-z0-9_]{36,255}": r"ghs_[A-Za-z0-9_]{36,255}",
    "new-format aware    ghs_[A-Za-z0-9._]{36,}": r"ghs_[A-Za-z0-9._]{36,}",
}
for name, rx in patterns.items():
    red = re.sub(rx, "[REDACTED]", line)
    m = re.search(rx, line)
    left = 0
    if m:
        start = line.index(t)
        end = start + len(t)
        left = max(0, end - m.end()) + max(0, m.start() - start)
    else:
        left = len(t)
    print(f"{name:52s} matched={'yes' if m else 'no ':3s} match_len={len(m.group(0)) if m else 0:4d} token_chars_left_visible={left}")
