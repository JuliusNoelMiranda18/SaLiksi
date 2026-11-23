import json, random
from common import *
items = []
for r in load_round(1):
    for i, a in enumerate(r["articles"]):
        items.append((f"1-{r['qid']}-{i}", r["group"], r["query"], a))
random.Random(42).shuffle(items)
# mixed across groups: take proportional-ish by round robin over groups
by = {}
for it in items: by.setdefault(it[1], []).append(it)
pick = []; order = ["international", "local", "edge"]; k = 0
while len(pick) < 50 and any(by.values()):
    g = order[k % 3]; k += 1
    if by.get(g): pick.append(by[g].pop())
random.Random(43).shuffle(pick)
md = ["# Human relevance check (50 papers)\n",
      "Score each paper: **2** = directly about the query topic (a student could cite it for that topic), **1** = related but not the main point, **0** = off-topic.\n",
      "Write your score after `Score:` for each. Do not look at any other file.\n"]
for n, (key, g, q, a) in enumerate(pick, 1):
    ab = (a.get("abstract") or "").strip()[:1500] or "no abstract"
    md.append(f"\n---\n## {n}. `{key}`\n**Query:** {q}\n\n**Title:** {a.get('title')}\n**Journal:** {a.get('journal')} ({a.get('year')})\n\n**Abstract:** {ab}\n\n**Score:** \n")
open("human_check.md", "w").write("\n".join(md))
print(len(pick), "papers written")
