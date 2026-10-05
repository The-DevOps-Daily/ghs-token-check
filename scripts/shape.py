"""Print the structure of a GitHub token without printing the token."""
import base64, json, os, re

t = os.environ["TOKEN"]
print("length:", len(t))
print("prefix:", t[:4])
print("separators (index, char):", [(i, c) for i, c in enumerate(t) if not c.isalnum()])
m = re.fullmatch(r"ghs_(\d+)_([^.]+)\.([^.]+)\.([^.]+)", t)
if not m:
    print("shape: legacy or unknown")
    raise SystemExit(0)
app_id, h, p, s = m.groups()
print("app id segment:", app_id, "(public: the app's numeric id)")
print("segment lengths header/payload/signature:", len(h), len(p), len(s))
print("chars used outside [A-Za-z0-9]:", sorted(set(re.sub(r"[A-Za-z0-9]", "", h + p + s))))

def b64(x):
    return base64.urlsafe_b64decode(x + "=" * (-len(x) % 4))

print("header:", b64(h).decode())
claims = json.loads(b64(p))
print("payload claim names:", sorted(claims))
if "iat" in claims and "exp" in claims:
    print("exp - iat (s):", claims["exp"] - claims["iat"])
print("signature bytes:", len(b64(s)))
