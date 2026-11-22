"""Deterministic field check (spec 5a) + heuristic style pre-check (5b draft).
Usage: python3 -I fieldcheck.py  -> fieldcheck.json   (judge verdicts are written separately by judge.py)
"""
import json, os, re, unicodedata, html
D = os.path.dirname(os.path.abspath(__file__))
STYLES = ("apa", "mla", "chicago")
MINOR = set("a an the and but or nor for so yet as at by in of on per to up via vs with from into onto over than".split())

def norm(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s or ""))
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    s = s.lower().replace("&", " and ").replace("–", "-").replace("—", "-").replace("‐", "-").replace("‑", "-")
    s = s.replace("ß", "ss").replace("ø", "o").replace("æ", "ae").replace("ł", "l").replace("đ", "d").replace("ı", "i")
    s = re.sub(r"[\W_]+", " ", s)
    return " ".join(s.split())

def has(hay, needle):
    n = norm(needle)
    return bool(n) and (" " + n + " ") in (" " + hay + " ")

def fam(a): return a.get("family") or a.get("name") or ""

def required_authors(auth, style):
    n = len(auth)
    if style == "apa": return auth if n <= 20 else auth[:19] + [auth[-1]]
    if style == "mla": return auth if n <= 2 else auth[:1]
    return auth if n <= 10 else auth[:7]   # Chicago 17: >10 authors -> first seven + et al.

def in_order(hay, names):
    pos = 0
    for nm in names:
        n = norm(nm)
        if not n: continue
        i = (" " + hay + " ").find(" " + n + " ", pos)
        if i < 0: return False
        pos = i + len(n)
    return True

def first_given_ok(s, a, style):
    g = (a.get("given") or "").strip()
    if not g: return True
    h = norm(s); f = norm(fam(a)); g1 = norm(g).split()
    if not g1: return True
    if style == "apa": return (" " + f + " " + g1[0][0] + " ") in (" " + h + " ")
    return (" " + f + " " + g1[0] + " ") in (" " + h + " ") or (" " + f + " " + g1[0][0] + " ") in (" " + h + " ")

def tail_numbers(s, t):
    """numbers in the string after removing authors, title, journal, DOI/URLs -> candidate source fields"""
    x = re.sub(r"https?://\S+|doi:\s*\S+|10\.\d{4,}/\S+", " ", s, flags=re.I)
    h = norm(x)
    for piece in [t["title"], t.get("subtitle"), t["container_title"]] + [fam(a) + " " + (a.get("given") or "") for a in t["authors"]]:
        n = norm(piece)
        if n: h = (" " + h + " ").replace(" " + n + " ", " ")
    h = re.sub(r"\b(accessed|retrieved)\b.*", " ", h)
    return [canon(x) for x in re.findall(r"\b[a-z]?\d+[a-z]?\b", h)]

def canon(x): return (x.lstrip("0") or "0") if x.isdigit() else x
def numtoks(v): return [canon(x) for x in norm(v).split() if re.search(r"\d", x)]

def check(s, t, style):
    errs, fab = [], []
    if not s or s.strip() in ("", "Citation unavailable."):
        return {"fields": {}, "errors": ["api_error"], "fabricated": []}
    h = norm(s); A = t["authors"]
    f = {}
    req = [fam(a) for a in required_authors(A, style)]
    f["authors"] = in_order(h, req) and first_given_ok(s, A[0], style)
    if not in_order(h, req):
        errs.append("author_truncated" if in_order(h, req[:min(len(req), 3)]) else "authors_wrong")
    elif not first_given_ok(s, A[0], style): errs.append("initials_wrong")
    if re.search(r"unknown author", s, re.I): fab.append("author:Unknown Author")
    yr = str(t["year"])
    f["year"] = yr in re.findall(r"(?<!\d)(\d{4})(?!\d)", re.sub(r"https?://\S+|10\.\d{4,}/\S+", " ", s))
    if not f["year"]: errs.append("wrong_year")
    f["title"] = has(h, t["title"])
    if not f["title"]: errs.append("title_altered")
    f["journal"] = has(h, t["container_title"])
    if not f["journal"]: errs.append("abbreviated_journal" if t["container_title"] else "journal_missing")
    nums = tail_numbers(s, t)
    allowed = {yr}
    for k, tag in (("volume", "missing_volume"), ("issue", "missing_issue")):
        v = t.get(k)
        if v:
            vt = numtoks(v) or norm(v).split()
            ok = bool(vt) and all(p in nums for p in vt)
            f[k] = bool(ok); allowed |= set(vt)
            if not ok: errs.append(tag)
        else: f[k] = None
    pg = t.get("page")
    if pg:
        parts = numtoks(pg) or norm(pg).split(); allowed |= set(parts)
        ok = all(p in nums for p in parts)
        if not ok and style in ("mla", "chicago") and len(parts) == 2 and parts[0] in nums:
            # MLA 9 / CMOS 9.61 allow abbreviated inclusive page numbers (1587-89)
            ends = [x for x in nums if x.isdigit() and parts[1].isdigit() and len(x) < len(parts[1]) and parts[1].endswith(x)]
            if ends: ok = True; allowed.add(ends[0])
        # accept abbreviated end page (e.g. 123-30) only as a style issue, not field pass
        f["pages"] = ok
        if not ok: errs.append("missing_pages")
    else: f["pages"] = None
    if t.get("article_number"): allowed |= set(numtoks(t["article_number"]))
    for x in ("17", "7", "9", "2025", "20"):  # don't count style names like 'APA 7' if echoed
        pass
    extra = [n for n in nums if n not in allowed]
    # year-like numbers (n.d. is fine) and volume/issue/page-like numbers not in the record
    if extra:
        if any(re.fullmatch(r"(19|20)\d\d", n) for n in extra): fab.append("year:" + ",".join(n for n in extra if re.fullmatch(r"(19|20)\d\d", n)))
        others = [n for n in extra if not re.fullmatch(r"(19|20)\d\d", n)]
        if others: fab.append("vol_issue_pages:" + ",".join(others))
    if not t.get("volume") and re.search(r"\bvol\.", s, re.I): fab.append("volume")
    if not t.get("page") and re.search(r"\bpp?\.\s*\d", s): fab.append("pages")
    dois = [d.lower().rstrip(".,;)") for d in re.findall(r"10\.\d{4,}/[^\s\"<>]+", s)]
    f["doi"] = t["DOI"].lower() in [d.lower() for d in dois] or t["DOI"].lower() in s.lower()
    if not f["doi"]: errs.append("no_doi")
    for d in dois:
        if d != t["DOI"].lower() and not t["DOI"].lower().startswith(d): fab.append("doi:" + d)
    if "n.d." in s and t["year"]: errs.append("nd_fallback")
    for k, tag in (("year", "invented_year"),):
        pass
    for fb in fab:
        tag = {"year": "invented_year", "vol_issue_pages": "invented_number", "volume": "invented_volume", "pages": "invented_pages", "doi": "invented_doi", "author": "invented_author"}[fb.split(":")[0]]
        if tag not in errs: errs.append(tag)
    return {"fields": f, "errors": errs, "fabricated": fab}

# ── heuristic style pre-check (reviewed by hand in judge.py) ─────────────────
def title_seg(s, t):
    m = re.search(r"[\"“](.+?)[\"”]", s)
    return m.group(1) if m else None

def cap_profile(seg):
    words = re.findall(r"[^\W\d_][\w'\-]*", re.sub(r"<[^>]+>", "", seg or ""))
    body = words[1:]
    longw = [w for w in body if w.lower() not in MINOR and len(w) > 3 and not w.isupper()]
    caps = sum(1 for w in longw if w[0].isupper()); return caps, len(longw)

def style_flags(s, t, style):
    fl = []; n = len(t["authors"])
    if not s: return ["api_error"], None
    variant = None
    if style == "apa":
        if not re.search(r"\(\s*(\d{4}|n\.d\.)[^)]*\)\.", s): fl.append("wrong_punctuation:year")
        if n >= 2 and n <= 20 and "&" not in s: fl.append("wrong_punctuation:ampersand")
        if n >= 21 and not re.search(r"\.\.\.|…", s): fl.append("et_al_rule:apa_21plus")
        if re.search(r"et al", s, re.I) and n <= 20: fl.append("et_al_rule:apa")
        # sentence case: title segment between "). " and next ". " roughly
        m = re.search(r"\)\.\s+(.+?)\.\s", s)
        if m:
            c, L = cap_profile(m.group(1))
            if L >= 3 and c / L > 0.6: fl.append("wrong_cap_rule:apa_title_case")
        if t.get("volume") and t.get("issue") and not re.search(r"\d+[A-Za-z]?\s*\(\s*[A-Za-z0-9\-\u2013/ ]+\)\s*[,.]", s): fl.append("wrong_punctuation:vol_issue")
        if m and re.search(r":\s+[a-z]", m.group(1)): fl.append("wrong_cap_rule:apa_after_colon")
    elif style == "mla":
        if n >= 3 and not re.search(r"et al\.", s): fl.append("et_al_rule:mla")
        if n == 2 and "et al" in s: fl.append("et_al_rule:mla")
        seg = title_seg(s, t)
        if not seg: fl.append("wrong_punctuation:title_quotes")
        else:
            c, L = cap_profile(seg)
            if L >= 2 and c / L < 0.6: fl.append("wrong_cap_rule:mla_sentence_case")
        if t.get("volume") and "vol." not in s: fl.append("wrong_punctuation:vol")
        if t.get("issue") and "no." not in s: fl.append("wrong_punctuation:no")
        pm = re.match(r"\s*(\w+)\s*[-–]\s*(\w+)", t.get("page") or "")
        if pm and pm.group(1) != pm.group(2) and "pp." not in s: fl.append("wrong_punctuation:pp")
    else:
        seg = title_seg(s, t)
        if not seg: fl.append("wrong_punctuation:title_quotes")
        else:
            c, L = cap_profile(seg)
            if L >= 2 and c / L < 0.6: fl.append("wrong_cap_rule:chicago_sentence_case")
        yr = str(t["year"])
        pre = s.split(seg)[0] if seg else s
        variant = "author-date" if yr in pre else ("notes-bibliography" if re.search(r"\(\s*" + yr + r"\s*\)", s) else "unclear")
        if n > 10 and not re.search(r"et al\.", s): fl.append("et_al_rule:chicago_10plus")
    if style in ("mla", "chicago") and n >= 2 and (style == "chicago" or n == 2):
        pers = [x for x in t["authors"] if x.get("family")]
        a2 = pers[1] if len(pers) > 1 else {}; g2 = norm(a2.get("given") or ""); f2 = norm(a2.get("family") or "")
        h = " " + norm(s) + " "
        if len(pers) > 1 and g2 and f2 and (" " + f2 + " " + g2 + " ") in h and (" " + g2 + " " + f2 + " ") not in h and (" " + g2.split()[0] + " " + f2 + " ") not in h and (" " + g2[0] + " " + f2 + " ") not in h:
            fl.append("wrong_name_order")
    if re.search(r"(?:accessed|retrieved)\s+(?:\d{1,2}\s+)?(?:[a-z]+\.?\s+)?(?:\d{1,2},?\s+)?2025", s, re.I): fl.append("invented_access_date")
    if t.get("article_number") and not t.get("page") and not has(norm(s), t["article_number"]): fl.append("missing_article_number")
    if re.search(r"\):\s*(https?:|doi|$)", s) or re.search(r",\s*,", s): fl.append("wrong_punctuation:empty_slot")
    return fl, variant

# CrossRef "author" entries that are job titles/affiliations, not authors (judge decision, listed in REPORT.md)
NOT_AUTHORS = {("ra028", 0), ("ra041", 0), ("ra041", 2)}

if __name__ == "__main__":
    truth = json.load(open(f"{D}/truth.json"))
    urls = {u["id"]: u for u in json.load(open(f"{D}/urls.json"))}
    out = {}
    for fn in sorted(os.listdir(f"{D}/raw")):
        r = json.load(open(f"{D}/raw/{fn}")); rid = r["run_id"]
        base = rid.split("__")[0]; tid = urls[base]["doi_id"] if base in urls else base
        t = dict(truth[tid]); t["authors"] = [a for k, a in enumerate(t["authors"]) if (tid, k) not in NOT_AUTHORS]; rec = {"run_id": rid, "truth_id": tid, "status": r["status"], "latency_s": r["latency_s"]}
        for st in STYLES:
            c = check(r.get(st), t, st); fl, var = style_flags(r.get(st), t, st)
            if r["status"] != 200: c = {"fields": {}, "errors": ["api_error" if "url" not in r["input"] else "fetch_failed"], "fabricated": []}
            rec[st] = {**c, "style_flags": fl, "variant": var}
        out[rid] = rec
    json.dump(out, open(f"{D}/fieldcheck.json", "w"), indent=1, ensure_ascii=False)
    print(len(out), "records")
