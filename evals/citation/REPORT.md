# SaLiksi citation engine eval: APA 7 / MLA 9 / Chicago 17

Run date: 2026-11-23 · Endpoint `POST /api/citation` on `localhost:3000` · Spec: [`evals/CITATION_EVAL.md`](../CITATION_EVAL.md)
One run, no tuning, no re-runs. The test set was frozen before the first call (`FROZEN.sha256`, 01:25:32 PST). Nothing under `saliksi/` was edited.

## Headline

**20 of 100 real papers (20.0%, 95% Wilson CI 13.3–28.9%) got all three citations (APA, MLA and Chicago) fully correct, checked against CrossRef records.**

Each style on its own is right about half the time. Most errors are style-rule mistakes, not lost data: when the paper data is checked alone, all three strings keep it intact for 77% of papers.

### What this does and does not prove
For DOI inputs the engine fetches the **same** CrossRef record used as ground truth. So these numbers measure **formatting fidelity**: does the model keep authors, year, title, journal, volume, issue, pages and DOI intact and apply the style rules? They do not measure whether retrieval finds the right paper. The URL inputs are the independent check, and they scored 0/20 (see below).

## Metrics

| Metric | Value | 95% CI |
|---|---|---|
| **Paper-level accuracy** (all 3 styles correct) | **20 / 100 = 20.0%** | 13.3–28.9 |
| N (DOI inputs evaluated) | **100** (8 candidate DOIs dropped before freezing, listed below) | |
| APA 7 accuracy | 50 / 100 = 50.0% | 40.4–59.6 |
| MLA 9 accuracy | 49 / 100 = 49.0% | 39.4–58.7 |
| Chicago 17 accuracy | 49 / 100 = 49.0% | 39.4–58.7 |
| Field check passes, all 3 styles (data intact, style ignored) | 77 / 100 = 77.0% | 67.8–84.2 |
| Paper-level, *if* capitalization rules are ignored (sensitivity only) | 38 / 100 = 38.0% | 29.1–47.8 |
| Fabricated-field rate (DOI, year, volume, issue, pages, author not in CrossRef) | 0 / 300 citations = 0.0% | |
| Strings with a hard-coded, false "Accessed/Retrieved 2025" date (not in the spec's fabrication list) | 10 / 300 (3.3%) | |
| **URL-path paper accuracy** | **0 / 20 = 0.0%** | 0–16.1 |
| URL path: fabricated-field rate (mostly "Unknown Author", invented year 2025) | 38 / 60 citations = 63.3% | |
| Avg latency (DOI) | 2.72 s (max 5.26 s) | |
| HTTP errors | 0 / 150 calls | |

### Per-field pass rate (DOI inputs, all three styles pooled, only where CrossRef has the field)
| authors | year | title | journal | volume | issue | pages | doi |
|---|---|---|---|---|---|---|---|
| 89.0% | 100% | 99.0% | 100% | 100% | 98.8% | 96.7% | 100% |

Field checks pass per style: APA 77%, MLA 95%, Chicago 90%. APA's author field is the weak point (see error pattern 2).

### By group
| Group | N | Paper-level | APA | MLA | Chicago |
|---|---|---|---|---|---|
| Random CrossRef journal articles | 50 | 22.0% (12.8–35.2) | 56% | 50% | 60% |
| Philippine research (OpenAlex, PH institutions) | 30 | 16.7% (7.3–33.6) | 36.7% | 60% | 43.3% |
| Hard edge cases | 20 | 20.0% (8.1–41.6) | 55% | 30% | 30% |

The Philippine set is OpenAlex's top PH-affiliated works, many of them big consortium papers (Global Burden of Disease, with 100–1,400 authors). That explains its weak APA score.

### URL path (20 open-access landing pages, same CrossRef truth)
The same 20 papers given as DOIs scored 2/20 paper-level. Given as URLs they scored 0/20.

| What happened | Count | Items |
|---|---|---|
| Engine fetched a **bot-check / CAPTCHA page and cited it as the paper** ("Making sure you're not a bot!", "Checking your browser - reCAPTCHA", "Bot Detection") | 6 | Ura024, Ura036, Uph007, Uph014, Uph021, Uph026 |
| No metadata at all → "Unknown Author / n.d. / URL as title" fallback | 7 | Ura002, Ura018, Uph002, Uph017, Uph027, Ued001, Ura010 |
| Metadata found, but volume/issue/pages missing (`fetchHtmlMeta` never extracts them) | 5 | Uph016, Ued003, Ued016, Ura009, Ura012 |
| Metadata found, only article number missing | 2 | Ura003, Ura043 |

I re-fetched each URL myself (`url_diag.json`, generic User-Agent). Results: 3 returned 403, 1 timed out, 3 had no `citation_*` tags, and 13 served full `citation_*` tags to my client. The engine's own fetch (Googlebot User-Agent, 8 s timeout) still got bot walls on several of those 13, so the HTML path loses data the page actually has. The engine doesn't log which step failed, so the categories above are inferred from the output strings.

### Repeat-run variance (10 DOIs × 4 runs)
- 4 of 10 items flip their paper-level verdict between runs. Paper accuracy over all 40 runs is 25%, versus 20% on first runs only.
- Only 2 of 30 style slots gave the identical string in all 4 runs. Typical flips: MLA/Chicago title case on one run and not the next (ra014, ra029), Chicago switching between notes-bibliography and author-date, and "Accessed 2025" appearing at random (ra018, ra032).
- Chicago variant across the 100 first runs: 54 author-date, 45 notes-bibliography, 1 unclear. The engine has no fixed Chicago variant.

## Top error tags (DOI inputs; count = style strings)

| Tag | Count | Examples |
|---|---|---|
| `wrong_cap_rule` MLA/Chicago kept CrossRef's sentence case (needs title case) | 30 MLA + 28 Chicago | ra003, ra005, ra008 |
| `missing_article_number` (e-locator such as e202301684 or 151482 dropped) | 18 | ra003, ra004, ra043 |
| `wrong_cap_rule` APA kept title case (needs sentence case) | 18 | ra009, ra016, ra026 |
| `author_truncated` / `et_al_rule` APA 21+ authors (no "…, last author") | 16 / 16 | ph003, ph004, ph009 |
| `et_al_rule` MLA listed all 3+ authors instead of "First, et al." | 15 | ra011, ra018, ra036 |
| `authors_wrong` (group author or compound surname dropped, "et al." in APA) | 12 | ra002, ph005, ph022 |
| `invented_access_date` "Accessed 2025" | 10 | ra014, ra022, ra026 |
| `wrong_cap_rule` APA: no capital after a colon | 9 | ra003, ph007, ra041 |
| `et_al_rule` Chicago >10 authors listed in full (CMOS 17: first 7 + et al.) | 9 | ra010, ph010, ph014 |
| `wrong_name_order` Chicago/MLA co-authors inverted ("Kana Sop, Marie Modestine") | 8 | ra021, ph004, ph006 |

## The 3 biggest error patterns and their likely causes in `saliksi/app/api/citation/route.ts`

1. **Capitalization and list rules applied inconsistently (about 60% of all style errors).** The model does all the formatting, and nothing checks its output in code. The prompt names the styles ("APA 7th, MLA 9th, Chicago 17th") but gives no rules, and it says "Use the data exactly as given". That pushes the model to copy CrossRef's title casing as-is: APA keeps title case, while MLA and Chicago keep sentence case. The same instruction-free design produces the MLA "et al." misses and the random Chicago variant. A small deterministic formatter would remove most of this (see phase 2 in the spec).
2. **Big author lists break.** `fetchCrossRef` passes only `w.author.slice(0, 30)` and then "; et al.". For any paper with more than 30 authors, APA 7's "first 19 … last author" rule can't be met, because the last author never reaches the model. Group authors with only a `name` field (ATLAS, GTEx, NCEAS) are mapped to `"" + …` and come out as an empty string, so they vanish. Truncating the author list also gives the model no cue to apply MLA's or Chicago's own cutoffs.
3. **Hard-coded fallbacks leak into good results.** The prompt line `"URL sources without metadata: cite as a webpage with access date 2025"` shows up as "Accessed 2025" on **DOI** inputs that have full metadata, and the date is false in 2026. On the URL path the `"Unknown Author" / "n.d."` rule, plus no check that the fetched page is a real article page, turns bot walls into confident citations of "Making sure you're not a bot!". `fetchHtmlMeta` never reads `citation_volume`, `citation_issue`, `citation_firstpage` or `citation_lastpage`, so even successful URL fetches can't produce a complete citation. Also, `formatMeta` only prints Issue/Pages when Volume exists, and article numbers (`article-number`) are never passed. That's the probable cause of the 18 missing article numbers. The "infer from DOI pattern" fallback never fired: every DOI resolved in CrossRef.

## What limits trust in these numbers
- **CrossRef overlap.** The DOI truth is the same record the engine reads, so "verified against CrossRef records" is accurate wording and "independently verified" is not.
- **Mixed models.** `lib/groq.ts` falls back through `openai/gpt-oss-120b` → `qwen/qwen3.8-27b` → `openai/gpt-oss-20b`, and the endpoint doesn't say which one answered. Results are a mix. (`lib/groq.ts` also has uncommitted local edits to that model list.)
- **Single judge.** Style verdicts come from one agent judge (me): regex style checks, then a hand review with documented overrides in `judge_overrides.json`. The blind re-judge of 10 items agreed on 30/30 style strings. That is an upper bound on reliability, since it's the same judge and the same rules. **The 10 items in `human_check.md` need your labels before the number is defensible in an interview.**
- **Strict style reading.** The judge applies the rules literally (MLA title case, CMOS 17's 10-author rule, APA capital after a colon, article numbers). A lenient grader would score higher: ignoring capitalization alone gives 38%. Italics can't be judged at all, because the output is plain text (a few strings use `*Journal*` markdown).
- **Judge calls on bad CrossRef data.** Affiliation strings stored as authors (ra028 #0; ra041 #0 and #2) were excluded from truth. ra015 (full name in `family`) and ra048 (Arabic names romanized) were accepted. Non-English titles (ed009, ed013, ed019, ra002, ra048) were allowed sentence case in MLA and Chicago. ra050 was a regex false positive. Two errors the normalized field check missed were added by hand: ed012 (diacritics dropped from "Kokoszyńska") and ed010 (article number 169).
- **Small N.** CIs are wide (±8 pp at the headline, ±16 pp for the URL path).
- **Edge-case selection.** Edge cases were chosen by rule from CrossRef/OpenAlex queries and random samples (`build_sets.py`), not hand-picked from memory, so every DOI is real. The "colon/markup" bucket got 2 `<i>`-title items plus 1 ChemInform title.
- **URL list.** 16 URLs came from OpenAlex OA landing pages and 4 from following the doi.org redirect. I removed a Springer `?error=cookies_not_supported` query from one URL before freezing.

### Dropped before freezing (no usable CrossRef record)
Random: 10.1021/ezv011i004_1789310, 10.1176/appi.pn.1986.21.15.3, 10.1017/s0038713400003742, 10.1080/00091383.1985.9940555, 10.1097/01.back.0000515451.72915.f1, 10.1080/00947598.1974.10394611 (missing title, author, year or container). Philippine: 10.1038/ng.2797, 10.1056/nejmoa2023184 (missing in CrossRef or no usable author field). Full list in `dropped.json`. No item was dropped after results were seen.

## Resume line (measured)
> Built a citation engine that pulls paper details from CrossRef, Semantic Scholar and web-page metadata. It produced fully correct APA, MLA and Chicago citations for **20%** of **100** real papers (all three styles; ~50% per style), verified against CrossRef records.

More useful framings of the same data: "kept bibliographic data intact in 77% of papers, with 0% fabricated fields on DOI input", or a phase-2 before/after story where a deterministic formatter fixes the style errors.

## Files
- Inputs: `dois.json`, `truth.json`, `urls.json`, `dropped.json`, `FROZEN.sha256`, `run_plan.json`, `build.log`
- Raw outputs: `raw/<id>.json` (150 files), `run.log`
- Scoring: `fieldcheck.py` → `fieldcheck.json`; `judge_overrides.json` + `judge.py` → `judge/<id>.json`; `metrics.py` → `metrics.json`
- Self-check: `rejudge_ids.json`, `judge_second/`; `human_check.md` (fill in); `url_diag.json`
- Scripts: `build_sets.py`, `extend_urls.py`, `run_eval.py`, `review.py`, `url_diag.py`, `make_human_check.py`
