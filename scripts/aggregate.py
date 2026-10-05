"""Summarise SAMPLE lines from a sample.yml run log: python3 scripts/aggregate.py results/samples.jsonl"""
import collections, json, sys
from patterns import load

rows = [json.loads(l) for l in open(sys.argv[1])]
print(f"tokens: {len(rows)}, new format: {sum(r['new_format'] for r in rows)}")
print("lengths:", dict(collections.Counter(r["length"] for r in rows)))
print("JWT part contains '-' or '_':", sum(r.get("jwt_has_dash") or r.get("jwt_has_underscore") for r in rows))
print("distinct 46-char heads:", len(set(r.get("head_sha256_8") for r in rows)))
print(f"{'pattern':20s} {'fully redacted':>15s} {'max chars visible':>18s}")
for name, _ in load():
    v = [r[name] for r in rows]
    print(f"{name:20s} {sum(x == 0 for x in v):>9d}/{len(v):<5d} {max(v):>18d}")
