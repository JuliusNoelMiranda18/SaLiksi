import json, random, re, glob
from common import *
R = random.Random(2026); B = 10000
J = json.load(open("judgments.json"))["judgments"]; C = json.load(open("credlabels.json"))
rounds = {r: load_round(r) for r in (1, 2, 3)}
def pct(xs, p):  # linear interpolation
    xs = sorted(xs); k = (len(xs) - 1) * p; f = int(k); c = min(f + 1, len(xs) - 1)
    return xs[f] + (xs[c] - xs[f]) * (k - f)
def ci(vals): vals = sorted(vals); return [vals[int(.025 * len(vals))], vals[int(.975 * len(vals)) - 1]]
# per-query records (round 1)
Q = []
for r in rounds[1]:
    rec = dict(qid=r["qid"], group=r["group"], n=0, rel2=0, rel1=0, cred=0, unk=0, both=0, judged=0, ok=0)
    for i, a in enumerate(r["articles"]):
        k = f"1-{r['qid']}-{i}"; s = J.get(k, {}).get("score"); c = C.get(k, {}).get("label")
        rec["n"] += 1; rec["judged"] += s is not None
        rec["rel2"] += s == 2; rec["rel1"] += (s is not None and s >= 1)
        rec["cred"] += c == "credible"; rec["unk"] += c == "unknown"; rec["both"] += (s == 2 and c == "credible")
        rec["ok"] += (s == 2 and c == "credible")
    Q.append(rec)
def ratio(qs, num, den="n"):
    d = sum(q[den] for q in qs); return sum(q[num] for q in qs) / d if d else float("nan")
def boot(qs, f):
    vals = []
    for _ in range(B):
        s = [R.choice(qs) for _ in qs]; v = f(s)
        if v == v: vals.append(v)
    return ci(vals)
def block(qs):
    o = {"queries": len(qs), "papers": sum(q["n"] for q in qs)}
    for name, num in (("credible_precision", "both"), ("relevance_score2", "rel2"), ("relevance_score_ge1", "rel1"),
                      ("credibility_credible", "cred"), ("unknown_rate", "unk")):
        o[name] = {"value": ratio(qs, num), "ci95": boot(qs, lambda s, n=num: ratio(s, n))}
    o["zero_result_queries"] = [q["qid"] for q in qs if q["n"] == 0]
    o["share_queries_with_1_relevant_credible"] = sum(q["both"] > 0 for q in qs) / len(qs)
    o["credible_precision_excluding_unknown"] = None
    return o
M = {"quality_round1": {"all": block(Q)}}
for g in ("international", "local", "edge"): M["quality_round1"][g] = block([q for q in Q if q["group"] == g])
M["quality_round1"]["judge_failures"] = sum(q["n"] - q["judged"] for q in Q)
# credibility excluding unknown
known = [(k, v) for k, v in C.items() if v["label"] != "unknown"]
M["credible_rate_excluding_unknown"] = sum(v["label"] == "credible" for k, v in known) / max(1, len(known))
# latency
S = [s for r in rounds.values() for s in r]
def lat(ss):
    t = [s["seconds"] for s in ss]
    if not t: return None
    return {"n": len(t), "p50": pct(t, .5), "p50_ci95": ci([pct([R.choice(t) for _ in t], .5) for _ in range(B)]),
            "p95": pct(t, .95), "p95_ci95": ci([pct([R.choice(t) for _ in t], .95) for _ in range(B)])}
M["latency"] = {"all": lat(S)}
for g in ("international", "local", "edge"): M["latency"][g] = lat([s for s in S if s["group"] == g])
M["search_success_rate"] = sum(s["status"] == 200 and len(s["articles"]) >= 1 for s in S) / len(S)
arts = [a for s in S for a in s["articles"]]
M["scoring_success_rate"] = sum((a.get("credibility") or 0) > 0 for a in arts) / max(1, len(arts))
M["slowest5"] = [(s["qid"], s["round"], round(s["seconds"], 1), s["status"]) for s in sorted(S, key=lambda s: -s["seconds"])[:5]]
M["errors"] = [(s["qid"], s["round"], s["status"], s["error"]) for s in S if s["error"] or s["status"] != 200]
# human agreement
try:
    txt = open("human_check.md").read(); H = {}
    for m in re.finditer(r"`(1-[A-Z0-9]+-\d+)`.*?\*\*Score:\*\*\s*([012])?", txt, re.S):
        if m.group(2) is not None: H[m.group(1)] = int(m.group(2))
    pairs = [(H[k], J[k]["score"]) for k in H if J.get(k, {}).get("score") is not None]
    if pairs:
        n = len(pairs); po = sum(a == b for a, b in pairs) / n
        pe = sum((sum(a == c for a, _ in pairs) / n) * (sum(b == c for _, b in pairs) / n) for c in (0, 1, 2))
        M["human_agreement"] = {"n": n, "exact_match": po, "kappa": (po - pe) / (1 - pe) if pe < 1 else None,
                                "human_relevant_rate": sum(a == 2 for a, _ in pairs) / n, "judge_relevant_rate_same": sum(b == 2 for _, b in pairs) / n}
except FileNotFoundError: pass
json.dump(M, open("metrics.json", "w"), indent=1); print(json.dumps(M, indent=1))
