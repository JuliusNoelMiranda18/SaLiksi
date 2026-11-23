# Rule (frozen before labeling): credible = venue.type in {journal, conference} AND (is_in_doaj OR is_core)
# AND not on Beall's list (exact match after normalizing journal or host org name).
# Unknown = no DOI/no match, PHILJOL, repository venue, preprint work type.
import json, time, urllib.request, urllib.error, urllib.parse, os
from common import *
UA = {"User-Agent": "saliksi-eval/1.0"}
def get(url):
    for i in range(5):
        time.sleep(1)
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(5 * (i + 1))
        except Exception:
            time.sleep(5 * (i + 1))
    return None
pred = {}
for l in open("predatory.txt"):
    if l.startswith("#") or "\t" not in l: continue
    tag, name = l.rstrip("\n").split("\t", 1); pred[norm(name)] = name
SEL = "select=id,doi,title,type,primary_location"
def resolve(a):
    if "philjol" in (a.get("source") or "").lower() or (a.get("journal") or "").lower() == "philjol":
        return None, "philjol"
    doi = a.get("doi")
    if doi: return get(f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi, safe='/:')}?{SEL}"), "doi"
    if (a.get("id") or "").startswith("https://openalex.org/W"):
        return get(f"https://api.openalex.org/works/{a['id'].split('/')[-1]}?{SEL}"), "oaid"
    t = a.get("title") or ""
    r = get("https://api.openalex.org/works?per-page=5&" + urllib.parse.urlencode({"search": t}) + "&" + SEL)
    for w in (r or {}).get("results", []):
        if norm(w.get("title")) == norm(t): return w, "title"
    return None, "nomatch"
out = {}
for r in load_round(1):
    for i, a in enumerate(r["articles"]):
        key = f"1-{r['qid']}-{i}"
        w, how = resolve(a)
        if how == "philjol": out[key] = {"label": "unknown", "why": "PHILJOL"}; continue
        src = ((w or {}).get("primary_location") or {}).get("source")
        if not w or not src:
            out[key] = {"label": "unknown", "why": f"no venue ({how})"}; continue
        json.dump(w, open(f"sources/{key}.json", "w"), indent=1)
        hit = [pred[n] for n in (norm(src.get("display_name")), norm(src.get("host_organization_name"))) if n and n in pred]
        if hit: out[key] = {"label": "not_credible", "why": "predatory list", "match": hit, "venue": src.get("display_name")}; continue
        if src.get("type") == "repository" or w.get("type") == "preprint":
            out[key] = {"label": "unknown", "why": f"repository/preprint ({src.get('type')}/{w.get('type')})", "venue": src.get("display_name")}; continue
        ok = src.get("type") in ("journal", "conference") and (src.get("is_in_doaj") or src.get("is_core"))
        out[key] = {"label": "credible" if ok else "not_credible", "venue": src.get("display_name"), "type": src.get("type"),
                    "doaj": src.get("is_in_doaj"), "core": src.get("is_core"), "why": "rule"}
    json.dump(out, open("credlabels.json", "w"), indent=1)
    print(r["qid"], len(out), flush=True)
