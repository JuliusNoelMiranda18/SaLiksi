"""Print compact review view for ids [start:end] of completed raw files. Usage: python3 -I review.py ra012 ra025"""
import json, sys, os
D = os.path.dirname(os.path.abspath(__file__))
fc = json.load(open(f"{D}/fieldcheck.json")); t = json.load(open(f"{D}/truth.json"))
ids = sys.argv[1:]
for rid in ids:
    if rid not in fc: continue
    r = json.load(open(f"{D}/raw/{rid}.json")); T = t[fc[rid]["truth_id"]]
    au = T["authors"]
    print(f"## {rid} n={len(au)} first={au[0]['family']},{au[0]['given']} last={au[-1]['family']} | {T['year']} | {T['title'][:90]} | {T['container_title']} | v={T['volume']} i={T['issue']} p={T['page']} an={T['article_number']}")
    for st in ("apa", "mla", "chicago"):
        x = fc[rid][st]
        print(f" {st[0].upper()}: {r[st]}\n    F{x['errors']} X{x['fabricated']} S{x['style_flags']} {x['variant'] or ''}")
