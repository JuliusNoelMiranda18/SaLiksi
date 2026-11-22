"""Compute metrics from judge/ verdicts + fieldcheck.json. Usage: python3 -I metrics.py -> metrics.json"""
import json, os, math, collections
D = os.path.dirname(os.path.abspath(__file__))
dois = json.load(open(f"{D}/dois.json")); urls = json.load(open(f"{D}/urls.json"))
fc = json.load(open(f"{D}/fieldcheck.json")); plan = json.load(open(f"{D}/run_plan.json"))
J = {f[:-5]: json.load(open(f"{D}/judge/{f}")) for f in os.listdir(f"{D}/judge")}
S = ("apa", "mla", "chicago")

def wilson(k, n, z=1.96):
    if n == 0: return (0, 0)
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0, 100 * (c - h)), 1), round(100 * (c + h), 1))
def ok(v, st): return v[st]["fields_ok"] and v[st]["style_ok"]
def paper_ok(v): return all(ok(v, st) for st in S)
def pct(k, n): return round(100 * k / n, 1) if n else None

def block(ids):
    n = len(ids); k = sum(paper_ok(J[i]) for i in ids)
    r = {"n": n, "paper_correct": k, "paper_accuracy": pct(k, n), "wilson95": wilson(k, n)}
    for st in S:
        c = sum(ok(J[i], st) for i in ids); r[f"{st}_accuracy"] = pct(c, n); r[f"{st}_wilson95"] = wilson(c, n)
        r[f"{st}_fields_ok"] = pct(sum(J[i][st]["fields_ok"] for i in ids), n); r[f"{st}_style_ok"] = pct(sum(J[i][st]["style_ok"] for i in ids), n)
    fields = collections.defaultdict(lambda: [0, 0])
    for i in ids:
        for st in S:
            for f, val in fc[i][st]["fields"].items():
                if val is None: continue
                fields[f][1] += 1; fields[f][0] += bool(val)
            if not fc[i][st]["fields"]:
                for f in ("authors", "year", "title", "journal", "doi"): fields[f][1] += 1
    r["per_field"] = {f: {"pass": a, "of": b, "pct": pct(a, b)} for f, (a, b) in fields.items()}
    fabc = sum(1 for i in ids for st in S if any(x.startswith(st + ":") for x in J[i]["fabricated_fields"]))
    r["fabricated_citation_rate"] = {"citations_with_fabrication": fabc, "of": 3 * n, "pct": pct(fabc, 3 * n)}
    lat = [fc[i]["latency_s"] for i in ids]; r["latency_avg_s"] = round(sum(lat) / n, 2); r["latency_max_s"] = max(lat)
    tags = collections.Counter(); ex = collections.defaultdict(list)
    for i in ids:
        for st in S:
            for e in set(J[i][st]["errors"]):
                tags[e] += 1
                if len(ex[e]) < 3 and i not in [x[0] for x in ex[e]]: ex[e].append((i, st))
    r["error_tags"] = [{"tag": t, "count": c, "examples": ex[t]} for t, c in tags.most_common()]
    r["chicago_variants"] = dict(collections.Counter(J[i]["chicago"]["variant"] for i in ids))
    r["status_counts"] = dict(collections.Counter(str(fc[i]["status"]) for i in ids))
    return r

doi_ids = [d["id"] for d in dois]; url_ids = [u["id"] for u in urls]
M = {"doi_all": block(doi_ids), "url_all": block(url_ids)}
for g in ("random", "philippine", "edge"): M["doi_" + g] = block([d["id"] for d in dois if d["group"] == g])
# URL vs paired DOI
M["url_vs_paired_doi"] = {"doi_paper_accuracy_same_20": block([u["doi_id"] for u in urls])["paper_accuracy"]}
# repeat variance
rv = []
for i in plan["repeat_ids"]:
    runs = [i] + [f"{i}__rep{k}" for k in (1, 2, 3)]
    rv.append({"id": i, "paper_ok": [paper_ok(J[r]) for r in runs],
               **{f"{st}_ok": [ok(J[r], st) for r in runs] for st in S},
               **{f"{st}_distinct_strings": len({json.load(open(f'{D}/raw/{r}.json'))[st] for r in runs}) for st in S}})
flips = sum(1 for x in rv if len(set(x["paper_ok"])) > 1)
allruns = [b for x in rv for b in x["paper_ok"]]
M["repeat_variance"] = {"items": rv, "items_whose_paper_verdict_flips": flips, "of": len(rv),
                        "paper_accuracy_over_all_40_runs": pct(sum(allruns), len(allruns)),
                        "paper_accuracy_first_run_only": pct(sum(x["paper_ok"][0] for x in rv), len(rv))}
json.dump(M, open(f"{D}/metrics.json", "w"), indent=1)
a = M["doi_all"]; print("DOI paper acc", a["paper_accuracy"], a["wilson95"], {s: a[f"{s}_accuracy"] for s in S}, "URL", M["url_all"]["paper_accuracy"])
