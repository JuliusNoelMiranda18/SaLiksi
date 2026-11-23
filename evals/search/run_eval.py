import json, random, time, urllib.request, urllib.error, os, sys
Q = json.load(open("queries.json"))
URL = "http://localhost:3000/api/research"
def search(q):
    body = json.dumps({"query": q["query"], "localSourcesOnly": q["localSourcesOnly"], "page": 1}).encode()
    req = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
    t = time.perf_counter(); status = None; arts = []; err = None
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            status = r.status; arts = json.loads(r.read()).get("articles", [])
    except urllib.error.HTTPError as e:
        status = e.code; err = str(e)
    except Exception as e:
        err = repr(e)
    dt = time.perf_counter() - t
    if err and ("timed out" in err.lower() or "timeout" in err.lower()): dt = 60.0
    return status, dt, arts, err
def save(rnd, q, res, warm=False):
    status, dt, arts, err = res
    name = "warmup.json" if warm else f"{rnd}-{q['id']}.json"
    json.dump({"qid": q["id"], "group": q["group"], "query": q["query"], "round": rnd, "status": status,
               "seconds": dt, "articles": arts, "error": err}, open("raw/" + name, "w"), indent=1)
    print(name, status, round(dt, 1), len(arts), err or "", flush=True)
save(0, Q[0], search(Q[0]), warm=True); time.sleep(20)
for rnd in (1, 2, 3):
    order = Q[:]; random.Random(1000 + rnd).shuffle(order)
    for q in order:
        save(rnd, q, search(q)); time.sleep(20)
