"""One sample per job: token shape and how much each pattern leaves visible. Prints no secret material."""
import hashlib, json, os, re
from patterns import load

t = os.environ["TOKEN"]
m = re.fullmatch(r"ghs_(\d+)_([^.]+)\.([^.]+)\.([^.]+)", t)
row = {"length": len(t), "new_format": bool(m)}
if m:
    jwt = ".".join(m.groups()[1:])
    row["jwt_has_dash"] = "-" in jwt
    row["jwt_has_underscore"] = "_" in jwt
    head = t.split(".")[0]  # ghs_<app id>_<base64url JWT header>
    row["head_len"] = len(head)
    row["head_sha256_8"] = hashlib.sha256(head.encode()).hexdigest()[:8]
for name, rx in load():
    mm = re.search(rx, t)
    row[name] = len(t) - (len(mm.group(0)) if mm else 0)
print("SAMPLE " + json.dumps(row))
