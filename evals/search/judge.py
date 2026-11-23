# usage: judge.py pilot | judge.py round1
import json, sys, os, time, urllib.request, urllib.error
from common import *
MODEL = "openai/gpt-oss-safeguard-20b"
KEY = [l.split("=",1)[1].strip().strip("\"'") for l in open("../../saliksi/.env.local") if l.startswith("GROQ_API_KEY=")][0]
RUBRIC = """You are grading search results for a student's research query.
Score the paper against the query:
2 = Directly about the query topic; a student could cite it for that topic.
1 = Related: same field or one part of the topic, but not the main point.
0 = Off-topic.
Reply with ONLY JSON: {"score": 0|1|2, "reason": "<one short sentence>"}"""
def judge(query, a):
    abstract = (a.get("abstract") or "").strip()[:1500] or "no abstract"
    prompt = f"{RUBRIC}\n\nQuery: {query}\n\nTitle: {a.get('title')}\nJournal: {a.get('journal')}\nYear: {a.get('year')}\nAbstract: {abstract}"
    body = json.dumps({"model": MODEL, "temperature": 0, "max_tokens": 1500,
        "messages": [{"role": "user", "content": prompt}]}).encode()
    for attempt in range(5):
        req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", body,
            {"Content-Type": "application/json", "Authorization": "Bearer " + KEY})
        try:
            txt = json.loads(urllib.request.urlopen(req, timeout=60).read())["choices"][0]["message"]["content"]
            s = txt[txt.index("{"):txt.rindex("}")+1]
            d = json.loads(s)
            if d["score"] in (0, 1, 2): return d
        except urllib.error.HTTPError as e:
            time.sleep(10 * (attempt + 1))
        except Exception:
            time.sleep(3)
    return {"score": None, "reason": "judge failed"}
mode = sys.argv[1]
rnd = 2 if mode == "pilot" else 1
items = []
for r in load_round(rnd):
    for i, a in enumerate(r["articles"]):
        items.append({"key": f"{rnd}-{r['qid']}-{i}", "query": r["query"], "a": a})
if mode == "pilot":
    import random; random.Random(7).shuffle(items); items = items[:20]
out = {}
fn = "pilot_judgments.json" if mode == "pilot" else "judgments.json"
for it in items:
    d = judge(it["query"], it["a"]); out[it["key"]] = d
    print(it["key"], d["score"], "|", it["a"]["title"][:60], "|", d["reason"][:80], flush=True)
    json.dump({"model": MODEL, "judgments": out}, open(fn, "w"), indent=1)
    time.sleep(3)
