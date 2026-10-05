"""One sample: token length, non-alphanumeric characters inside the JWT, and regex coverage. No secret printed."""
import json, os, re

t = os.environ["TOKEN"]
m = re.fullmatch(r"ghs_(\d+)_([^.]+)\.([^.]+)\.([^.]+)", t)
row = {"length": len(t), "new_format": bool(m)}
if m:
    jwt = ".".join(m.groups()[1:])
    row["jwt_dash"] = "-" in jwt
    row["jwt_underscore"] = "_" in jwt
    import hashlib
    head = t.split(".")[0]  # ghs_<app id>_<base64url header>
    row["head_len"] = len(head)
    row["head_sha256_8"] = hashlib.sha256(head.encode()).hexdigest()[:8]
rx = {
    "legacy": r"ghs_[0-9a-zA-Z]{36}",
    "underscore36": r"(ghu|ghs)_[A-Za-z0-9_]{36}",
    "open_ended": r"ghs_[A-Za-z0-9_]{36,255}",
    "github_may15": r"ghs_[A-Za-z0-9\._]{36,}",
    "github_may26": r"ghs_[A-Za-z0-9\.\-_]{36,}",
    "gitleaks_pr2193": r"(?:ghu_[0-9a-zA-Z]{36}|ghs_(?:[0-9a-zA-Z]{36}|[0-9]+_eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+))",
    "trufflehog_pr5156": r"\b(ghs_[0-9]+_eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]+|(?:ghp|gho|ghu|ghs|ghr|github_pat)_[a-zA-Z0-9_]{36,255}\b)",
    "full_jwt": r"ghs_\d+_[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
}
for k, r in rx.items():
    mm = re.search(r, t)
    row[k + "_visible"] = len(t) - (len(mm.group(0)) if mm else 0)
print("SAMPLE " + json.dumps(row))
if os.environ.get("MASK_TEST") == "1" and m:
    print("MASKTEST header segment alone:", m.group(2))
    print("MASKTEST app id prefix alone:", "ghs_" + m.group(1) + "_")
