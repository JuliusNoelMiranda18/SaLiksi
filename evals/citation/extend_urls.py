"""Second pass for urls.json: for OA items whose landing URL was doi.org, follow the doi.org redirect to the publisher page."""
import json, os, time, urllib.request, urllib.parse
D = os.path.dirname(os.path.abspath(__file__)); UA = {"User-Agent": "saliksi-eval/1.0"}
items = json.load(open(f"{D}/dois.json")); urls = json.load(open(f"{D}/urls.json"))
have = {u["doi_id"] for u in urls}
for it in items:
    if len(urls) >= 20: break
    if it["id"] in have: continue
    try:
        r = json.loads(urllib.request.urlopen(urllib.request.Request("https://api.openalex.org/works/doi:" + urllib.parse.quote(it["doi"]), headers=UA), timeout=30).read())
    except Exception: continue
    time.sleep(1)
    if not (r.get("open_access") or {}).get("is_oa"): continue
    try:
        final = urllib.request.urlopen(urllib.request.Request("https://doi.org/" + it["doi"], headers=UA, method="HEAD"), timeout=30).geturl()
    except urllib.error.HTTPError as e: final = e.url if hasattr(e, "url") else None
    except Exception: final = None
    time.sleep(1)
    if final and "doi.org" not in final:
        urls.append({"id": "U" + it["id"], "doi_id": it["id"], "url": final, "group": it["group"], "via": "doi.org redirect"})
        print(it["id"], final)
json.dump(urls, open(f"{D}/urls.json", "w"), indent=1, ensure_ascii=False)
print("urls", len(urls))
