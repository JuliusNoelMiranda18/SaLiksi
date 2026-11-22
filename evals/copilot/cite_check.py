"""Deterministic citation check (spec 5a). Usage: python3 -I cite_check.py -> citations.json"""
import json, os, re, glob, unicodedata, html
D = os.path.dirname(os.path.abspath(__file__))
vault = json.load(open(f"{D}/vault.json"))
def norm(s): return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().replace(".", "").strip()
SRC = [{"id": v["id"], "year": str(v["year"]), "first": norm(v["authors"][0]["lastName"]),
        "all": [norm(a["lastName"]) for a in v["authors"]], "n": len(v["authors"])} for v in vault]
NAME = r"(?:[A-Z][\w'\-]+(?:\s(?:Jr\.|[A-Z][\w'\-]+))?|de la [A-Z][\w\-]+)"
AUTH = rf"{NAME}(?:(?:,\s*{NAME})*(?:,?\s*(?:&|and)\s*{NAME})|(?:,\s*{NAME})*,?\s+et al\.?)?"
ONE = re.compile(rf"^(?P<auth>{AUTH})(?P<sep>,?)\s*(?P<year>\d{{4}}[a-z]?|n\.d\.)?(?:,?\s*(?:p+\.\s*)?(?P<page>\d+(?:[-–]\d+)?))?$")
NARR = re.compile(rf"(?P<auth>{AUTH})\s*\((?P<year>\d{{4}})\)")

def parse_auth(a):
    etal = "et al" in a
    a = re.sub(r"\s+et al\.?", "", a)
    names = [x.strip() for x in re.split(r",\s*|\s*&\s*|\s+and\s+", a) if x.strip()]
    return names, etal, ("&" in a), (" and " in a)

def match(names, year, fmt):
    f = norm(names[0])
    for s in SRC:
        if s["first"] == f and (fmt == "MLA" and year is None or year == s["year"]):
            return s["id"], "first_author"
    for s in SRC:  # lenient: surname is any author of a source (+ year if given)
        if f in s["all"] and (year is None or year == s["year"]):
            return s["id"], "non_first_author"
    return None, None

def extract(text, fmt):
    text = html.unescape(text or "")  # model sometimes emits &amp;
    # tag content without parentheses, e.g. <INLINE_CITATION>Smith, 2023</INLINE_CITATION>, is still a citation
    text = re.sub(r"<INLINE_CITATION>\s*([^()<]+?)\s*</INLINE_CITATION>", r"[TAG](\1)", text)
    text = re.sub(r"</?INLINE_CITATION>", "", text)
    text = re.sub(r"[\u00a0\u202f\u2009\u2007]", " ", text)  # model emits narrow no-break spaces in "et al."
    cits = []
    for m in re.finditer(r"\(([^()]{2,200})\)", text):
        for part in m.group(1).split(";"):
            part = part.strip()
            if re.fullmatch(r"[A-Z0-9\-]+s?", part): continue  # acronyms like (DO), (TDS)
            mm = ONE.match(part)
            if not mm: continue
            if fmt == "APA" and not mm.group("year"): continue  # APA citations always carry a year; drops (FiSAT), (Sources 1-8)
            if not (mm.group("year") or mm.group("page") or "et al" in part or re.fullmatch(NAME, part)): continue
            if not mm.group("year") and re.fullmatch(r"[A-Z][a-z]+", part) and part not in [n for s in vault for n in [a["lastName"] for a in s["authors"]]]:
                continue  # single capitalised word like (Microcystis) is not a citation
            tag = text[max(0, m.start()-5):m.start()] == "[TAG]"
            cits.append({"raw": f"({part})", "kind": "tag_no_parens" if tag else "parenthetical", **mm.groupdict()})
    for mm in NARR.finditer(text):
        cits.append({"raw": mm.group(0), "kind": "narrative", "auth": mm.group("auth"), "sep": "", "year": mm.group("year"), "page": None})
    return cits

def check_format(c, fmt, sid):
    names, etal, amp, andw = parse_auth(c["auth"])
    n = next((s["n"] for s in SRC if s["id"] == sid), None)
    if fmt == "APA":
        if c["kind"] == "tag_no_parens": return False  # renders without parentheses
        if c["kind"] == "parenthetical" and not (c["year"] and c["sep"] == ","): return False
        if n is not None:
            if n >= 3 and not etal: return False
            if n == 2 and not (amp or andw) and c["kind"] == "parenthetical": return False
            if n == 2 and c["kind"] == "parenthetical" and not amp: return False
        return True
    if fmt == "MLA":
        if c["kind"] == "tag_no_parens": return False
        if c["year"] or c["sep"] == ",": return False
        if n is not None:
            if n >= 3 and not etal: return False
            if n == 2 and not andw: return False
        return True

out = {}
for f in sorted(glob.glob(f"{D}/raw/*.json")):
    r = json.load(open(f))
    rows = []
    for c in extract(r.get("response"), r["format"]):
        names, *_ = parse_auth(c["auth"])
        echo = not match(names, None, "MLA")[0] and re.sub(r"\W", "", c["raw"]).lower() in re.sub(r"\W", "", r["prompt"]).lower()
        sid, how = match(names, c["year"][:4] if c["year"] and c["year"][0].isdigit() else None, r["format"])
        rows.append({"raw": c["raw"], "kind": c["kind"], "matched_source": sid, "match_type": how,
                     "author_text": c["auth"], "year": c["year"], "echo_of_prompt": echo, "valid": how == "first_author", "format_ok": check_format(c, r["format"], sid)})
    out[r["run_id"]] = {"id": r["id"], "category": r["category"], "format": r["format"], "citations": rows}
json.dump(out, open(f"{D}/citations.json", "w"), indent=1)
allc = [c for v in out.values() for c in v["citations"]]
print("runs", len(out), "citations", len(allc), "valid", sum(c["valid"] for c in allc), "format_ok", sum(c["format_ok"] for c in allc))
