"""Send every eval prompt to /api/writer and save raw results. Usage: python3 -I run_eval.py"""
import json, os, random, time, urllib.request, urllib.error
D = os.path.dirname(os.path.abspath(__file__))
URL = "http://localhost:3000/api/writer"
vault = [{k: s[k] for k in ["id","title","authors","year","journal","abstract","doi","url"]} for s in json.load(open(f"{D}/vault.json"))]
prompts = json.load(open(f"{D}/prompts.json"))
rng = random.Random(42)
answerable = [p for p in prompts if p["category"] == "answerable"]
mla_ids = sorted(p["id"] for p in rng.sample(answerable, 10))
rep_ids = sorted(p["id"] for p in rng.sample(prompts, 10))
json.dump({"seed": 42, "mla_ids": mla_ids, "repeat_ids": rep_ids}, open(f"{D}/run_plan.json", "w"), indent=1)

def call(p, fmt):
    body = {"message": p["text"], "history": [], "action": "chat",
            "context": {"vaultSources": vault, "folderName": "EvalVault", "citationFormat": fmt, "documentContent": p.get("documentContent", "")}}
    data = json.dumps(body).encode()
    for attempt in range(4):
        t = time.time()
        try:
            r = urllib.request.urlopen(urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"}), timeout=180)
            return {"status": r.status, "latency_s": round(time.time()-t, 2), "response": json.loads(r.read())["response"], "attempts": attempt+1}
        except urllib.error.HTTPError as e:
            status, err = e.code, e.read().decode()[:300]
        except Exception as e:
            status, err = None, str(e)[:300]
        if status not in (429, 500, None) or attempt == 3:
            return {"status": status, "latency_s": round(time.time()-t, 2), "response": None, "error": err, "attempts": attempt+1}
        time.sleep(15 * 2**attempt)  # 15s, 30s, 60s: Groq free tier is 8k tokens/min per model

jobs = [(p, "APA", p["id"]) for p in prompts]
jobs += [(p, "MLA", f"{p['id']}__mla") for p in prompts if p["id"] in mla_ids]
jobs += [(p, "APA", f"{p['id']}__rep{k}") for p in prompts if p["id"] in rep_ids for k in (1, 2, 3)]
os.makedirs(f"{D}/raw", exist_ok=True)
for n, (p, fmt, rid) in enumerate(jobs, 1):
    out = f"{D}/raw/{rid}.json"
    if os.path.exists(out): continue
    res = call(p, fmt)
    json.dump({"run_id": rid, "id": p["id"], "category": p["category"], "format": fmt, "prompt": p["text"],
               "documentContent": p.get("documentContent", ""), **res}, open(out, "w"), indent=1, ensure_ascii=False)
    print(n, len(jobs), rid, res["status"], res["latency_s"], flush=True)
    time.sleep(12)  # ~4.3k tokens per call; 2s pacing hit the TPM limit in run 1
print("DONE")
