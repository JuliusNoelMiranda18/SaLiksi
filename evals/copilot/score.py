"""Compute metrics from judge/ + citations.json + raw/. Usage: python3 -I score.py -> metrics.json"""
import json, glob, os, math, collections, statistics
D = os.path.dirname(os.path.abspath(__file__))
def wilson(k, n, z=1.96):
    if n == 0: return (0, 0)
    p = k/n; d = 1 + z*z/n; c = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return (round(100*(c-h), 1), round(100*(c+h), 1))
prompts = {p["id"]: p for p in json.load(open(f"{D}/prompts.json"))}
J = {k: json.load(open(f"{D}/judge/{k}.json")) for k in prompts}
raw = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(f"{D}/raw/*.json")}
cits = json.load(open(f"{D}/citations.json"))
M = {}
g = [k for k in prompts if raw.get(k, {}).get("status") == 200 and J[k]["grounded"]]
M["N"] = len(prompts); M["grounded"] = len(g); M["grounded_pct"] = round(100*len(g)/len(prompts), 1); M["grounded_ci"] = wilson(len(g), len(prompts))
M["per_category"] = {}
for cat in ["answerable", "unanswerable", "adversarial"]:
    ids = [k for k in prompts if prompts[k]["category"] == cat]; k = sum(J[i]["grounded"] for i in ids)
    M["per_category"][cat] = {"n": len(ids), "grounded": k, "pct": round(100*k/len(ids), 1), "ci": wilson(k, len(ids))}
for st in ["single", "multi", "edit"]:
    ids = [k for k in prompts if prompts[k].get("subtype") == st]; k = sum(J[i]["grounded"] for i in ids)
    M["per_category"][f"answerable_{st}"] = {"n": len(ids), "grounded": k, "pct": round(100*k/len(ids), 1)}
# citation accuracy over the 60 judged APA runs
tot = val = sup = acc = 0; echoes = []
for k in prompts:
    bad = set(J[k]["citation_indexes_not_supporting"])
    for i, c in enumerate(cits[k]["citations"]):
        if c["echo_of_prompt"]: echoes.append((k, c["raw"])); continue
        tot += 1; val += c["valid"]; s = i not in bad; sup += s; acc += c["valid"] and s
M["citations_total"] = tot; M["citation_validity_pct"] = round(100*val/tot, 1); M["citation_support_pct"] = round(100*sup/tot, 1)
M["citation_accuracy"] = acc; M["citation_accuracy_pct"] = round(100*acc/tot, 1); M["citation_accuracy_ci"] = wilson(acc, tot)
M["excluded_prompt_echoes"] = echoes
M["fabricated_all_runs"] = [(k, c["raw"], c["match_type"]) for k, v in cits.items() for c in v["citations"] if not c["valid"] and not c["echo_of_prompt"]]
def fmt(runs):
    cs = [c for r in runs for c in cits[r]["citations"] if not c["echo_of_prompt"]]
    return {"n": len(cs), "ok": sum(c["format_ok"] for c in cs), "pct": round(100*sum(c["format_ok"] for c in cs)/len(cs), 1) if cs else None,
            "no_parens_tag": sum(c["kind"] == "tag_no_parens" for c in cs)}
M["format_APA_main60"] = fmt(list(prompts))
M["format_MLA_10"] = fmt([k for k in cits if k.endswith("__mla")])
plan = json.load(open(f"{D}/run_plan.json")); rep = json.load(open(f"{D}/judge/_repeats_and_mla.json"))["repeat_grounded"]
runs4 = {k: [J[k]["grounded"]] + [bool(x) for x in rep[k]] for k in plan["repeat_ids"]}
M["repeats"] = {"per_prompt": {k: f"{sum(v)}/4" for k, v in runs4.items()}, "fully_consistent_prompts": sum(len(set(v)) == 1 for v in runs4.values()),
                "grounded_over_40_runs": sum(sum(v) for v in runs4.values()),
                "mean_per_prompt_std_pct": round(100*statistics.mean(statistics.pstdev([float(x) for x in v]) for v in runs4.values()), 1)}
lat = [r["latency_s"] for r in raw.values() if r["status"] == 200]
M["latency"] = {"mean_s": round(statistics.mean(lat), 2), "median_s": round(statistics.median(lat), 2), "max_s": max(lat), "calls": len(raw),
                "errors_final": sum(r["status"] != 200 for r in raw.values()), "calls_needing_retry": sum(r.get("attempts", 1) > 1 for r in raw.values())}
M["failures"] = collections.Counter(J[k]["failure_type"] for k in prompts if not J[k]["grounded"])
M["failure_ids"] = {ft: [k for k in prompts if J[k]["failure_type"] == ft] for ft in M["failures"]}
agree = sum(json.load(open(f))["grounded"] == J[os.path.basename(f)[:-5]]["grounded"] for f in glob.glob(f"{D}/judge_second/*.json"))
M["self_agreement"] = f"{agree}/10"
json.dump(M, open(f"{D}/metrics.json", "w"), indent=1, ensure_ascii=False, default=list)
print(json.dumps(M, indent=1, ensure_ascii=False, default=list))
