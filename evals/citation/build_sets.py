"""Build and freeze the DOI and URL test sets plus CrossRef ground truth.
Usage: python3 -I build_sets.py   (writes dois.json, truth.json, urls.json, dropped.json, build.log)
Edge cases are chosen by rule from CrossRef/OpenAlex records (not from memory), so every DOI is real.
"""
import json, os, re, time, unicodedata, urllib.request, urllib.error, urllib.parse
D = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "saliksi-eval/1.0"}
LOG = open(f"{D}/build.log", "w")
def log(*a):
    print(*a, flush=True); print(*a, file=LOG, flush=True)

def get(url, tries=5):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                time.sleep(1); return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 404: time.sleep(1); return None
            if e.code not in (429, 500, 502, 503, 504): raise
        except Exception as e:
            log("retry", url, e)
        time.sleep(2 * 2 ** k)
    return None

def year_of(w):
    for k in ("published", "issued", "published-print"):
        dp = (w.get(k) or {}).get("date-parts") or [[None]]
        if dp[0] and dp[0][0]: return dp[0][0]
    return None

def truth_of(w):
    authors = [{"family": a.get("family"), "given": a.get("given"), "name": a.get("name")} for a in w.get("author", [])]
    return {"authors": authors, "year": year_of(w), "title": (w.get("title") or [None])[0],
            "subtitle": (w.get("subtitle") or [None])[0], "container_title": (w.get("container-title") or [None])[0],
            "volume": w.get("volume"), "issue": w.get("issue"), "page": w.get("page"),
            "article_number": w.get("article-number"), "DOI": w["DOI"].lower(), "type": w.get("type")}

def usable(w):
    return bool(w and w.get("title") and w["title"][0] and any(a.get("family") for a in w.get("author", []))
                and year_of(w) and w.get("container-title") and w["container-title"][0])

def strip(s): return "".join(c for c in unicodedata.normalize("NFKD", s or "") if not unicodedata.combining(c))

items, truth, seen, dropped, records = [], {}, set(), [], {}
def add(w, group, why=""):
    doi = w["DOI"].lower()
    if doi in seen: return False
    seen.add(doi); records[doi] = w
    items.append({"id": f"{group[:2]}{sum(1 for i in items if i['group']==group)+1:03d}", "doi": doi, "group": group, "why": why})
    truth[items[-1]["id"]] = truth_of(w); return True

# ── 1. Random journal articles (50) ───────────────────────────────────────────
pool = []
while sum(1 for i in items if i["group"] == "random") < 50:
    res = get("https://api.crossref.org/works?sample=100&filter=type:journal-article")
    for w in res["message"]["items"]:
        if sum(1 for i in items if i["group"] == "random") >= 50: pool.append(w); continue
        if usable(w): add(w, "random")
        else: dropped.append({"doi": w["DOI"], "group": "random", "reason": "unusable CrossRef record (missing title/author/year/container)"})
log("random", sum(1 for i in items if i["group"] == "random"))

# ── 2. Philippine research (30) ───────────────────────────────────────────────
oa = get("https://api.openalex.org/works?filter=institutions.country_code:PH,has_doi:true,type:article&per-page=50")
ph_oa = {}
for r in oa["results"]:
    if sum(1 for i in items if i["group"] == "philippine") >= 30: break
    doi = r["doi"].replace("https://doi.org/", "").lower()
    w = (get("https://api.crossref.org/works/" + urllib.parse.quote(doi)) or {}).get("message")
    if usable(w):
        if add(w, "philippine"): ph_oa[doi] = r
    else:
        dropped.append({"doi": doi, "group": "philippine", "reason": "no usable CrossRef record"})
log("philippine", sum(1 for i in items if i["group"] == "philippine"))

# ── 3. Edge cases (20), selected by rule from extra random samples ────────────
need = {"many_authors": 5, "article_number": 5, "accented_names": 4, "subtitle": 3, "markup_or_colon_title": 3}
got = {k: 0 for k in need}
def edge_kind(w):
    if not usable(w): return None
    n = len(w.get("author", []))
    t = w["title"][0]
    if n >= 21 and got["many_authors"] < 5: return "many_authors"
    if (w.get("article-number") or (w.get("page") and not re.search(r"\d+\s*-\s*\d+", w["page"]))) and not w.get("issue") and got["article_number"] < 5:
        return "article_number"
    names = " ".join((a.get("family") or "") + (a.get("given") or "") for a in w.get("author", []))
    if strip(names) != names and got["accented_names"] < 4: return "accented_names"
    if w.get("subtitle") and w["subtitle"][0] and got["subtitle"] < 3: return "subtitle"
    if re.search(r"<(i|sub|sup|em)>", t) and got["markup_or_colon_title"] < 3: return "markup_or_colon_title"
    return None

# 3a. 21+ authors are rare in random samples: query OpenAlex for multi-author articles, verify count in CrossRef
mo = get("https://api.openalex.org/works?filter=authors_count:%3E20,type:article,has_doi:true&sample=40&seed=7&per-page=40")
for r in (mo or {}).get("results", []):
    if got["many_authors"] >= 5: break
    doi = r["doi"].replace("https://doi.org/", "").lower()
    if doi in seen: continue
    w = (get("https://api.crossref.org/works/" + urllib.parse.quote(doi)) or {}).get("message")
    if usable(w) and len(w.get("author", [])) >= 21 and add(w, "edge", f"many_authors ({len(w['author'])} authors in CrossRef)"):
        got["many_authors"] += 1
# 3b. markup titles: CrossRef query for titles with chemical formulas/italics, verify tag present
mk = get("https://api.crossref.org/works?query.bibliographic=synthesis+crystal+structure+complex&filter=type:journal-article&rows=100")
for w in mk["message"]["items"]:
    if got["markup_or_colon_title"] >= 3: break
    if usable(w) and w["DOI"].lower() not in seen and re.search(r"<(i|sub|sup)>", w["title"][0]):
        if add(w, "edge", "markup_or_colon_title (title contains <i>/<sub>/<sup>)"): got["markup_or_colon_title"] += 1
# 3c. the rest from random samples
rounds = 0
while sum(got.values()) < 20 and rounds < 40:
    rounds += 1
    cand = pool if rounds == 1 else get("https://api.crossref.org/works?sample=100&filter=type:journal-article")["message"]["items"]
    for w in cand:
        if w["DOI"].lower() in seen: continue
        k = edge_kind(w)
        if k and add(w, "edge", k): got[k] += 1
log("edge", got, "rounds", rounds)

json.dump(items, open(f"{D}/dois.json", "w"), indent=1, ensure_ascii=False)
json.dump(truth, open(f"{D}/truth.json", "w"), indent=1, ensure_ascii=False)
json.dump(dropped, open(f"{D}/dropped.json", "w"), indent=1, ensure_ascii=False)

# ── 4. URL set (20): open-access landing pages from OpenAlex, not doi.org ─────
urls = []
for it in items:
    if len(urls) >= 20: break
    r = ph_oa.get(it["doi"]) or get("https://api.openalex.org/works/doi:" + urllib.parse.quote(it["doi"]))
    if not r or not (r.get("open_access") or {}).get("is_oa"): continue
    loc = r.get("best_oa_location") or r.get("primary_location") or {}
    u = loc.get("landing_page_url")
    if u and "doi.org" not in u:
        urls.append({"id": "U" + it["id"], "doi_id": it["id"], "url": u, "group": it["group"]})
json.dump(urls, open(f"{D}/urls.json", "w"), indent=1, ensure_ascii=False)
log("dois", len(items), "urls", len(urls), "dropped", len(dropped))
