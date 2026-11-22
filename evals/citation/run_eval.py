"""Send every frozen input to /api/citation sequentially; save raw/<run_id>.json. Usage: python3 -I run_eval.py (resumable)"""
import json, os, random, time, urllib.request, urllib.error
D = os.path.dirname(os.path.abspath(__file__)); URL = "http://localhost:3000/api/citation"
dois = json.load(open(f"{D}/dois.json")); urls = json.load(open(f"{D}/urls.json"))
rep_ids = sorted(i["id"] for i in random.Random(42).sample(dois, 10))
json.dump({"seed": 42, "repeat_ids": rep_ids}, open(f"{D}/run_plan.json", "w"), indent=1)

def call(body):
    data = json.dumps(body).encode()
    for attempt in range(4):
        t = time.time()
        try:
            r = urllib.request.urlopen(urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"}), timeout=180)
            j = json.loads(r.read())
            return {"status": r.status, "latency_s": round(time.time()-t, 2), "apa": j.get("apa"), "mla": j.get("mla"), "chicago": j.get("chicago"), "attempts": attempt+1}
        except urllib.error.HTTPError as e:
            status, err = e.code, e.read().decode()[:300]
        except Exception as e:
            status, err = None, str(e)[:300]
        if status not in (429, 500, None) or attempt == 3:
            return {"status": status, "latency_s": round(time.time()-t, 2), "apa": None, "mla": None, "chicago": None, "error": err, "attempts": attempt+1}
        time.sleep(10 * 2**attempt)

jobs = [(i["id"], {"doi": i["doi"]}) for i in dois]
jobs += [(u["id"], {"url": u["url"]}) for u in urls]
jobs += [(f"{i}__rep{k}", {"doi": next(x["doi"] for x in dois if x["id"] == i)}) for i in rep_ids for k in (1, 2, 3)]
os.makedirs(f"{D}/raw", exist_ok=True)
for n, (rid, body) in enumerate(jobs, 1):
    out = f"{D}/raw/{rid}.json"
    if os.path.exists(out): continue
    res = call(body)
    json.dump({"run_id": rid, "input": body, **res}, open(out, "w"), indent=1, ensure_ascii=False)
    print(n, len(jobs), rid, res["status"], res["latency_s"], flush=True)
    time.sleep(2)
print("DONE")
