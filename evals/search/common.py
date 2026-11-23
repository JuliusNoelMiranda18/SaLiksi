import json, glob, os, re
def load_round(r):
    out = []
    for f in sorted(glob.glob(f"raw/{r}-*.json")):
        out.append(json.load(open(f)))
    return out
def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", (s or "").lower())).strip()
