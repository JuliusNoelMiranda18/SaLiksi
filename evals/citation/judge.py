"""Write judge/<run_id>.json verdicts (spec 5b).
Style verdict = heuristic flags from fieldcheck.py, then the agent-judge's hand review in judge_overrides.json:
  {"<run_id>": {"<style>": {"add": ["tag", ...], "remove": ["tag", ...], "note": "..."}, "notes": "..."}}
Usage: python3 -I judge.py [outdir]   (default judge/)
"""
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.join(D, sys.argv[1] if len(sys.argv) > 1 else "judge")
fc = json.load(open(f"{D}/fieldcheck.json"))
ov = json.load(open(f"{D}/judge_overrides.json")) if os.path.exists(f"{D}/judge_overrides.json") else {}
os.makedirs(out_dir, exist_ok=True)
for rid, r in fc.items():
    o = ov.get(rid, {}); v = {"id": rid, "truth_id": r["truth_id"]}; fab = []
    for st in ("apa", "mla", "chicago"):
        x = r[st]; so = o.get(st, {})
        style_errs = [f for f in x["style_flags"] if f not in so.get("remove", [])] + [a for a in so.get("add", []) if a not in x["style_flags"]]
        field_errs = [e for e in x["errors"] if e not in so.get("remove", [])]
        fields_ok = bool(x["fields"]) and not field_errs
        v[st] = {"fields_ok": fields_ok, "style_ok": not style_errs and bool(x["fields"]),
                 "errors": field_errs + style_errs, "variant": x.get("variant"), "note": so.get("note", "")}
        fab += [f"{st}:{f}" for f in x["fabricated"] if f"{st}:{f}" not in o.get("unfabricate", [])]
    v["fabricated_fields"] = fab; v["notes"] = o.get("notes", "")
    json.dump(v, open(f"{out_dir}/{rid}.json", "w"), indent=1, ensure_ascii=False)
print(len(fc), "verdicts ->", out_dir)
