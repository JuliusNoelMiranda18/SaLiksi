"""Diagnose URL inputs independently: HTTP status + whether citation_* meta tags exist. Generic UA (engine itself sends a Googlebot UA)."""
import json, os, re, time, urllib.request, urllib.error
D = os.path.dirname(os.path.abspath(__file__))
out = {}
for u in json.load(open(f"{D}/urls.json")):
    t = time.time()
    try:
        r = urllib.request.urlopen(urllib.request.Request(u["url"], headers={"User-Agent": "saliksi-eval/1.0", "Accept": "text/html"}), timeout=8)
        h = r.read(800000).decode("utf-8", "ignore"); st = r.status
        out[u["id"]] = {"status": st, "citation_title": bool(re.search(r'name=["\']citation_title', h, re.I)),
                        "citation_author_count": len(re.findall(r'name=["\']citation_author["\']', h, re.I)),
                        "citation_doi": bool(re.search(r'name=["\']citation_doi', h, re.I))}
    except urllib.error.HTTPError as e: out[u["id"]] = {"status": e.code}
    except Exception as e: out[u["id"]] = {"status": None, "error": type(e).__name__ + ": " + str(e)[:80]}
    out[u["id"]]["secs"] = round(time.time() - t, 1); print(u["id"], out[u["id"]], flush=True); time.sleep(1)
json.dump(out, open(f"{D}/url_diag.json", "w"), indent=1)
