"""One sample: token length, non-alphanumeric characters inside the JWT, and regex coverage. No secret printed."""
import json, os, re

t = os.environ["TOKEN"]
m = re.fullmatch(r"ghs_(\d+)_([^.]+)\.([^.]+)\.([^.]+)", t)
row = {"length": len(t), "new_format": bool(m)}
if m:
    jwt = ".".join(m.groups()[1:])
    row["jwt_dash"] = "-" in jwt
    row["jwt_underscore"] = "_" in jwt
    row["prefix46_constant"] = t[:46]  # ghs_<app id>_<base64 header>: public, identical across tokens
rx = {
    "legacy": r"ghs_[0-9a-zA-Z]{36}",
    "underscore36": r"(ghu|ghs)_[A-Za-z0-9_]{36}",
    "open_ended": r"ghs_[A-Za-z0-9_]{36,255}",
    "dot_aware": r"ghs_[A-Za-z0-9._]{36,}",
    "full_jwt": r"ghs_\d+_[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
}
for k, r in rx.items():
    mm = re.search(r, t)
    row[k + "_visible"] = len(t) - (len(mm.group(0)) if mm else 0)
print("SAMPLE " + json.dumps(row))
