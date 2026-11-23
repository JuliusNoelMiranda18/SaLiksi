# Task for the agent: evaluate SaLiksi search (relevance, credibility, latency)

You are running an evaluation, not changing the product. Produce **honest** numbers for a resume bullet:

> Built an academic search over OpenAlex, Semantic Scholar and PHILJOL that returned relevant, peer-reviewed sources for **[P]%** of results across **[N]** queries at **[B]** s p95 latency.

Report whatever the numbers turn out to be. Do **not** tune the code, drop hard queries, change a rule after seeing results, or re-run until the numbers look good. A low score with a clear failure analysis is a valid result.

Before you start, read `SALIKSI-MINDMAP/00 Home.md`, `SALIKSI-MINDMAP/20 API/api-research.md`, `SALIKSI-MINDMAP/30 Lib/lib-credibility.md` and `SALIKSI-MINDMAP/50 External/ext-openalex.md`.

## 0. What is being tested

- **Endpoint:** `POST /api/research` (`saliksi/app/api/research/route.ts`). Body: `{ "query": "...", "localSourcesOnly": false, "page": 1 }`.
- **Response:** `{ articles: [{ title, authors, year, journal, abstract, doi, url, source, localSource, openAccess, citationCount, credibility }] }`, at most 10 articles.
- **How it works:** OpenAlex → PHILJOL (only on page 1, and only when the search is local-only or OpenAlex returned fewer than 5 results) → Semantic Scholar (international searches only). These run **one after another**. Results are deduplicated and capped at 10. Each one is then scored by the LLM in parallel (`lib/credibility.ts` → `lib/groq.ts`, 3-model fallback), and the list is sorted local-first, then by score.
- **Watch out:** the route returns HTTP 200 even when scoring failed, and sets `credibility: 0` for those papers. Count real scores, not status codes.
- **What this test proves:** whether what users see is on-topic and comes from credible venues, and how fast it arrives. It does **not** test whether the app's own credibility score is correct. That needs a separate labeled set of predatory and reputable venues.

## 1. Setup

1. `cd saliksi && npm install` if `node_modules` is missing.
2. The server needs `GROQ_API_KEY` in `saliksi/.env.local`. **If it isn't set, stop and ask the user. Never print or log it.**
3. Check the Groq account limits (requests per minute and per day) in the Groq console. The app makes about **900 Groq calls** (90 searches × about 10) and the relevance judge about **300 more**. If the daily limit is lower, stop and ask the user. They may split the run over two days; if so, note it in the report.
4. Use a production build: `npm run build && npm start` (port 3000), in the background. Not `npm run dev`, because dev mode compiles routes on the first request and inflates the slow tail. Confirm it answers before testing.
5. Put all work in `evals/search/`. **Do not edit anything under `saliksi/`.** Use Python with `-I`, standard library only.
6. Your scripts call OpenAlex directly for labeling. Use a generic `User-Agent` such as `saliksi-eval/1.0`. **Do not put the user's name or email in any request.** Make requests one at a time, about 1 s apart, with backoff on 429 or 5xx.
7. Record the git commit (`git rev-parse HEAD`), the date and time, and the machine.

## 2. Query set (`evals/search/queries.json`)

Write **30 queries** like a Filipino undergrad would type them, and **freeze the list before running anything**. Write `FROZEN.sha256` of the file. Never swap queries after seeing results.

| Group | Count | `localSourcesOnly` | Example |
|---|---|---|---|
| International topics | 15 | false | "machine learning crop yield prediction" |
| Local topics | 10 | true | "typhoon disaster preparedness Philippines" |
| Edge cases | 5 | false | one word, long sentence, Filipino words, a typo, a very rare topic |

Spread the topics over STEM, health, social science, education and business.

## 3. Run (`evals/search/run_eval.py`)

- Send **1 warm-up search** first and throw away the result.
- Then run **3 rounds × 30 queries = 90 searches**, one at a time. Shuffle the query order each round with a fixed seed.
- Wait **20 s between searches** so the run stays under Groq's per-minute limit. The full run takes about 40 minutes.
- Client timeout: 60 s. **Don't retry.** A failure or timeout is part of the result. A timed-out search counts as 60 s and as a failure.
- Save `evals/search/raw/<round>-<qid>.json`: query id, group, round, HTTP status, wall-clock seconds (`time.perf_counter` around the request), the full `articles` array, and the error text if any.
- **Latency** uses all 3 rounds. **Quality labeling** (sections 4–5) uses only **round 1**: up to 300 papers.

## 4. Relevance labels (`evals/search/judge.py`)

**Rubric (freeze before scoring):**

| Score | Meaning |
|---|---|
| 2 | Directly about the query topic; a student could cite it for that topic |
| 1 | Related: same field or one part of the topic, but not the main point |
| 0 | Off-topic |

- **Relevant = score 2.** Report "score ≥ 1" as a secondary number.
- Judge input: the query, plus the paper's title, abstract (the first 1,500 characters; write "no abstract" if empty), journal and year. Output JSON `{ "score": 0|1|2, "reason": "..." }`.
- Use a judge model that is **not** in the app's `MODELS` list in `lib/groq.ts` if one is available, so the app doesn't grade itself. Record the model name. Temperature 0.
- **Pilot first:** run the judge on 20 papers from round 2 (not the test set), read the results, fix the rubric wording once if it's unclear, then freeze it. Never change the rubric after scoring the round 1 papers.
- **Human check:** `make_human_check.py` picks **50** round 1 papers at random (fixed seed, mixed across groups) and writes them to `evals/search/human_check.md` **without** the judge's score. The user labels them. Then compute judge–human agreement: Cohen's kappa and % exact match. If kappa < 0.6, say in the report that the relevance number is unreliable, and also report relevance on the 50 human-labeled papers alone.

## 5. Credibility labels (`evals/search/credlabel.py`)

These come from outside facts, **not** the app's `credibility` score.

1. **Resolve each paper's venue in OpenAlex.**
   - Has a DOI: look up `https://api.openalex.org/works/doi:<doi>`, then its primary source.
   - OpenAlex result without a DOI: use the work id from the `id` field.
   - Semantic Scholar result with no DOI: search for the title and accept only an exact match after normalizing.
   - Save the source record in `evals/search/sources/`.
   - First, fetch one source record by hand and check which fields actually exist. Expected: `type`, `is_in_doaj`, `is_core`, `host_organization_name`. Adjust the rule below to the real field names **before** labeling anything, and write down what you used.
2. **Predatory list:** save an archived copy of Beall's list of journals and publishers to `evals/search/predatory.txt`, and record its source URL and date. Match journal and publisher names after normalizing (lowercase, no punctuation). Write every match to the report so a human can check it.
3. **Rule (freeze before labeling):** a paper is **credible** when
   - its venue type is a journal or conference, **and**
   - the venue is in DOAJ **or** is a core source in OpenAlex, **and**
   - it is not on the predatory list.
4. **Unknown:** no DOI and no match, PHILJOL items (the route sets journal = "PHILJOL" and loses the real journal name), repositories, and preprints. In the headline, **unknown counts as not credible** (the conservative choice). Report the unknown count separately, and report the rate with unknowns left out as a secondary number.

## 6. Metrics (`evals/search/metrics.py` → `metrics.json`)

**Quality (round 1):**
- **Credible precision (headline P):** papers that are relevant (score 2) **and** credible ÷ all returned papers.
- Relevance alone; credibility alone; unknown rate.
- All of the above, split by group (international / local / edge).
- Queries that returned 0 papers: list them. They add nothing to the numerator or denominator, so also report the share of queries with at least 1 relevant, credible paper.
- **95% confidence intervals** with a bootstrap that resamples **queries**, not papers (10,000 times). Papers from the same query are related, so resampling single papers would make the interval too narrow.

**Latency (all 3 rounds, 90 searches):**
- p50 and p95 with bootstrap 95% CIs (linear interpolation; say so), and split by group.
- Search success rate: HTTP 200 with at least 1 article.
- Scoring success rate: articles with `credibility > 0` ÷ all articles. A real score of exactly 0 is possible but rare; note this.

## 7. Report (`evals/search/REPORT.md`)

Include:
- Commit, date and time, machine, judge model, predatory-list source.
- A table of every metric with its CI.
- Judge–human agreement.
- 10 example failures: off-topic papers, non-credible papers and slow searches, each with the query.
- The 5 slowest searches.
- Every predatory match.
- The filled-in bullet, plus a one-line note on how to word it honestly.

Caveats to state:
- Relevance labels come from an LLM judge, checked against 50 human labels (give the kappa).
- Credibility uses indexing as a proxy (DOAJ, OpenAlex core, Beall's list). Good local journals that aren't indexed count as not credible, and Beall's list is old and disputed.
- Latency depends on live external APIs and the time of day. This is one run, at one time, on one machine, measured from a local client.
- 30 queries is a small set; quote the CI.
