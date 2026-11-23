# Plan: raise citation accuracy from 20%

Status: proposal, nothing built yet · Written 2026-11-23 · Based on [`REPORT.md`](REPORT.md) (first eval run)
Code touched: `saliksi/app/api/citation/route.ts`, plus a new `saliksi/lib/citationFormat.ts`

## 1. Where we are

| Measure (first run) | Value |
|---|---|
| Papers with all 3 styles correct (DOI input) | **20 / 100** |
| Correct per style (APA / MLA / Chicago) | 50% / 49% / 49% |
| Paper data kept intact (style ignored) | 77% |
| URL input, all 3 styles correct | **0 / 20** |

**The main finding.** Every one of the 80 failing DOI papers failed *only* on things code can control: capitalization, "et al." rules, name order, dropped article numbers, cut-off author lists and the fake "Accessed 2025". None of them failed because the data was missing. CrossRef already had what we needed. The LLM loses it or formats it wrong.

So the fix is not a better prompt. **Move formatting out of the LLM and into code.**

### What breaks, and how many papers each problem touches (out of 100)

| Problem | Papers | Root cause in `route.ts` |
|---|---|---|
| Wrong capitalization (APA wants sentence case; MLA/Chicago want title case) | 49 | The LLM copies CrossRef's casing ("Use the data exactly as given") |
| "et al." rules broken (MLA 3+, APA 21+, Chicago >10) | 35 | No rules in the prompt; the LLM guesses |
| Author list cut off (APA needs the last author) | 15 | `w.author.slice(0, 30)` drops everyone after 30 |
| Punctuation / layout (vol(issue), pp., empty slots) | 12 | The LLM guesses |
| Fake "Accessed 2025" | 8 | Hard-coded in the prompt: "access date 2025" |
| Co-authors' names inverted | 7 | The LLM guesses |
| Group authors dropped (ATLAS, GTEx) | 6 | `(a.family \|\| "")` gives an empty string when CrossRef has only `name` |
| Article number missing (e.g. e202301684) | 6 | `article-number` is never read; `formatMeta` only prints issue/pages when volume exists |
| Other (initials, diacritics, an invented journal name) | 5 | The LLM rewrites data |

On the URL path: 6 of 20 citations **cite a bot-check page as the paper**, 7 fall back to "Unknown Author", and the rest lack volume, issue and pages, because `fetchHtmlMeta` never reads them.

## 2. Target

Re-run the **same frozen 100 DOIs + 20 URLs** with the same judge rules, then report before and after side by side.

| Measure | Now | Target |
|---|---|---|
| DOI, all 3 styles correct | 20% | **≥ 75%** |
| DOI, data intact | 77% | ≥ 97% |
| URL, all 3 styles correct | 0% | ≥ 40% |
| Bot-wall pages cited as papers | 6 / 20 | **0** |
| Invented fields ("Unknown Author", "Accessed 2025", made-up years) | yes | **0** |
| Same input → same output | 2 / 30 strings stable | 30 / 30 |

Why 75% and not 100%: automatic casing has real limits. Turning a title-case title into APA sentence case needs to know which words are proper nouns ("Africa", "Aspergillus"). 18 papers fail *only* on casing, so casing quality decides most of the gap.

To avoid tuning to the test, also run a **fresh held-out sample** of 50 random CrossRef DOIs after the fix and report it separately (§ 6).

## 3. New design

```
input ──▶ resolve metadata ──▶ CitationRecord (typed, all fields) ──▶ formatApa / formatMla / formatChicago (pure code)
              │                        │
              │                        └─▶ titleCase(): code; sentenceCase(): small LLM call, checked, else keep original
              └─ DOI: CrossRef → Semantic Scholar
                 URL: find DOI in page/URL → CrossRef; else parse citation_* tags; bot wall → fail cleanly
                 nothing found → LLM fallback, clearly marked "unverified" (or ask the user for a DOI)
```

`CitationRecord` (new type in `lib/citationFormat.ts`):

```ts
type Person = { family: string; given?: string } | { group: string };  // group = "ATLAS Collaboration"
interface CitationRecord {
  authors: Person[];            // ALL authors, never cut off
  year?: string;                // published-print → published-online → issued (one fixed rule)
  title: string;                // HTML tags stripped (<i>, <sub>) → plain text with Unicode (CO₂)
  subtitle?: string;
  container?: string;           // journal, &amp; decoded
  volume?: string; issue?: string; pages?: string; articleNumber?: string;
  doi?: string; url?: string;
  language?: string;            // CrossRef `language` if present; used to skip re-casing
  source: "crossref" | "semanticscholar" | "html" | "llm";
}
```

The API keeps returning `{ apa, mla, chicago }`, so the citation page and the researcher page keep working. It also adds an optional `meta: { source, warnings[] }` that the UI can show later (for example "unverified: no metadata found").

## 4. Work plan

### Phase 1: Get all the data (small, low risk)
File: `route.ts` → `fetchCrossRef`, `formatMeta`

- [ ] Return structured authors: `{family, given}` per person, `{group: name}` when only `name` exists. **Remove `slice(0, 30)`.**
- [ ] Read `article-number`. Stop nesting issue and pages under volume.
- [ ] Strip HTML from titles and decode entities (`&amp;` → `&`), keeping chemical subscripts as Unicode.
- [ ] Pick one year rule and keep it (`published-print` → `published-online` → `issued`).
- [ ] Send an honest User-Agent. Optional: a `mailto` from an env var, for CrossRef's faster "polite pool".
- [ ] Skip author entries that are clearly affiliations ("Professor of…", "University…"), and add a warning when one is skipped.

*Fixes:* cut-off author lists (15), group authors (6), article numbers (6).

### Phase 2: Deterministic formatter (the big win)
New file: `saliksi/lib/citationFormat.ts` (pure functions, no network)

**Authors**
- APA 7: `Family, I. I.`, `&` before the last author; up to 20 authors list all; 21+ list the first 19, then `…`, then the last author. Initials handle hyphens (`Mei-Wei` → `M.-W.`) and particles (`de Kroon`, `van Langenberg`).
- MLA 9: 1 author `Family, Given.`; 2 authors `Family, Given, and Given Family.`; 3+ authors `Family, Given, et al.`
- Chicago 17 (bibliography): only the first author inverted; up to 10 authors list all; more than 10 list the first 7, then `et al.`
- Group authors print as-is (`ATLAS Collaboration`).
- Keep diacritics exactly as CrossRef gives them.

**Titles**
- `titleCase()` (MLA, Chicago, journal names): capitalize the first word, the last word and the word after a colon. Lowercase articles, prepositions, coordinating conjunctions and "to". **Never touch** words with internal capitals, digits or all caps (`ddCOSMO`, `CO₂`, `THP-1`, `ICT`). Handle hyphenated words.
- `sentenceCase()` (APA): this is the hard one. Recommended approach:
  1. If the title is already sentence case (few capitalized non-initial words), keep it.
  2. Otherwise make **one small LLM call** that may only change letter case. Check in code that `out.toLowerCase() === in.toLowerCase()`. If the check fails, keep the original title. Capitalize the word after a colon.
  3. Cache results by DOI so the same paper always gives the same output.
- Non-English titles (CrossRef `language` ≠ `en`, or a simple non-English-script check): keep the original casing in every style.

**Rest of the entry**
- APA: `Journal, vol(issue), pages. https://doi.org/…`. Use the article number when there are no pages. Use an en-dash in page ranges.
- MLA: `Journal, vol. X, no. Y, Year, pp. A–B. https://doi.org/….` Use `p.` for one page.
- Chicago: **choose one variant** (notes-bibliography) and always use it: `Journal Vol, no. Issue (Year): pages. https://doi.org/….`
- Never print empty slots (`(2024): https…`, `, ,`). Omit missing fields.
- **No access date** for anything with a DOI. For a real webpage with no metadata, use *today's* date from the server clock, not "2025".

Route change: when a `CitationRecord` exists, call the three formatters directly. No LLM except `sentenceCase()`.

*Fixes:* capitalization (49), et al. (35), punctuation (12), access date (8), name order (7), diacritics, made-up journal names, and run-to-run variance.

### Phase 3: Fix the URL path
File: `route.ts` → `fetchHtmlMeta`

- [ ] **Look for a DOI first.** Check the `citation_doi` / `dc.identifier` / `prism.doi` tags and the URL itself (Springer, MDPI and Wiley URLs contain it). If found, take the DOI path. 13 of the 20 test pages had full `citation_*` tags, most with a DOI.
- [ ] **Detect bot walls.** If the title or body matches `not a bot|captcha|checking your browser|just a moment|access denied|bot detection|cloudflare`, or the status is 403/429, treat it as a failed fetch, not as metadata.
- [ ] Parse `citation_volume`, `citation_issue`, `citation_firstpage`, `citation_lastpage`, `citation_journal_title` and `citation_publication_date`, plus all `citation_author` tags, into a `CitationRecord`.
- [ ] Stop pretending to be Googlebot. Bot protection checks that claim, and faking it gets blocked more often. Use a normal User-Agent string.
- [ ] If no DOI is found, try a Semantic Scholar or OpenAlex **title** search, and accept a match only if the titles agree closely (normalized similarity ≥ 0.9).
- [ ] If everything fails, return a clear error: *"Couldn't read this page. Paste the DOI instead."* Never return a citation with "Unknown Author / Unknown Title".

### Phase 4: Make the fallbacks honest
- [ ] Delete the prompt rules "access date 2025" and "infer from DOI pattern".
- [ ] Keep the LLM only for file uploads and plain-text input. Mark those results `meta.source = "llm"` and add a warning, so the UI can label them "unverified".

### Phase 5: Tests and cleanup
- [ ] Add `vitest` (dev dependency; there is no test runner yet). Unit-test the three formatters on ~20 fixture records copied from `evals/citation/truth.json`: 1, 2, 3, 21+ and 100+ authors, a group author, an article number, missing volume, a non-English title, a chemical-formula title.
- [ ] Update the dev-mode trace text on both pages: `citation/page.tsx` (~line 146) and `researcher/page.tsx` (~line 328) still say "sends a structured prompt to Groq LLM…".
- [ ] Don't build on the legacy `lib/citations.ts` without checking it. The vault lists it as dead code (`70 Issues/issues-dead-code.md`).
- [ ] Vault sync (per `CLAUDE.md`): update `20 API/api-citation.md`, add `30 Lib/lib-citationFormat.md` from the template, link it from `00 Home.md`, and log anything left in `70 Issues/issues-known.md`.

## 5. Order and effort

| # | Phase | Effort | Expected gain |
|---|---|---|---|
| 1 | Get all the data | ~2 h | Unlocks phase 2 |
| 2 | Deterministic formatter | ~1 day | Most of the jump (20% → ~70–85%) |
| 3 | URL path | ~0.5 day | 0% → ~40–60% on URLs; no more bot-wall citations |
| 4 | Honest fallbacks | ~1 h | No more invented fields |
| 5 | Tests + vault | ~0.5 day | Keeps it from breaking again |

Work on a branch (e.g. `citation-formatter`) and do one phase per commit, so a regression is easy to trace.

## 6. How we measure it (eval phase 2)

1. Keep the first run untouched (`raw/`, `judge/`, `metrics.json`).
2. Add an output-folder argument to `run_eval.py`, `fieldcheck.py`, `judge.py` and `metrics.py`, and write to `raw_after/`, `judge_after/` and `metrics_after.json`.
3. Re-run the **same frozen lists** (check `FROZEN.sha256` first) with the same judge rules and overrides.
4. Run a **fresh held-out set** of 50 new random CrossRef DOIs that nobody has looked at, to show the gain isn't fitted to the 100.
5. Report before / after / held-out side by side, with Wilson CIs, in `REPORT.md`.
6. Label `human_check.md` (both runs) so the numbers hold up in an interview.

If it works, the resume line becomes a before/after story:
> "…moved formatting from an LLM to a rule-based engine, raising fully correct APA/MLA/Chicago citations from 20% to X% on 100 real papers (Y% on a held-out set), verified against CrossRef records."

## 7. Risks

| Risk | Mitigation |
|---|---|
| APA sentence case gets proper nouns wrong | LLM limited to case-only changes, checked in code, original kept on failure; report casing errors as their own metric |
| Bad CrossRef data (affiliations as authors, full name in `family`) | Phase 1 filters plus warnings; can't be fixed fully, so count it in the report |
| Fitting the fix to the 100 test papers | The held-out 50-DOI set in § 6 |
| Publishers block every fetch | Find the DOI in the URL first; otherwise fail clearly instead of inventing |
| `{apa, mla, chicago}` contract breaks the two pages | Shape stays the same; `meta` is optional and extra |
