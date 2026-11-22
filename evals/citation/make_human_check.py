"""Write human_check.md: 10 random DOI items (seed 7) with truth, outputs and the judge's verdict for hand confirmation."""
import json, os, random
D = os.path.dirname(os.path.abspath(__file__))
dois = json.load(open(f"{D}/dois.json")); truth = json.load(open(f"{D}/truth.json"))
pick = sorted(random.Random(7).sample([d["id"] for d in dois], 10))
L = ["# Human check: citation eval", "",
     "Confirm or overturn the judge's verdict for each item. Put `Y` (agree) or `N` + reason in the **Your label** line.",
     "Rules: APA 7, MLA 9, Chicago 17 (either notes-bibliography or author-date), as in `evals/CITATION_EVAL.md` 5b.", ""]
for i in pick:
    d = next(x for x in dois if x["id"] == i); t = truth[i]; r = json.load(open(f"{D}/raw/{i}.json")); v = json.load(open(f"{D}/judge/{i}.json"))
    au = "; ".join(f"{a.get('family') or a.get('name')}, {a.get('given') or ''}".strip(", ") for a in t["authors"][:25]) + (f" … (+{len(t['authors'])-25} more)" if len(t["authors"]) > 25 else "")
    L += [f"## {i} ({d['group']}) · DOI `{d['doi']}`", "",
          "**CrossRef truth**", "",
          f"- authors ({len(t['authors'])}): {au}", f"- year: {t['year']}", f"- title: {t['title']}" + (f" — subtitle: {t['subtitle']}" if t.get("subtitle") else ""),
          f"- journal: {t['container_title']}", f"- volume {t['volume']} · issue {t['issue']} · pages {t['page']} · article no. {t['article_number']}", ""]
    for st in ("apa", "mla", "chicago"):
        x = v[st]
        verdict = "CORRECT" if x["fields_ok"] and x["style_ok"] else "WRONG: " + ", ".join(x["errors"])
        L += [f"**{st.upper()}**{' (' + x['variant'] + ')' if x.get('variant') else ''}", "", "> " + (r[st] or "(no output)"), "",
              f"Judge: {verdict}" + (f" — {x['note']}" if x.get("note") else ""), "", "Your label: ____", ""]
    if v["fabricated_fields"]: L += [f"Fabricated fields flagged: {', '.join(v['fabricated_fields'])}", ""]
    L += ["---", ""]
open(f"{D}/human_check.md", "w").write("\n".join(L)); print("human_check.md", pick)
