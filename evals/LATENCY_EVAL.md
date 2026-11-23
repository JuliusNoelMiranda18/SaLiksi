# Plan: search latency + model-failover test

Target bullet (fill in only with measured numbers):

> Made search faster and more reliable: p95 latency dropped from **[A]** s to **[B]** s, and the model-failover chain kept **[X]%** of requests succeeding under simulated rate limits.

This bullet claims a change ("dropped from A to B"), so this plan is **not** eval-only like `CITATION_EVAL.md`. It has three phases: measure baseline → make the change → measure again. Report the numbers as they come out. If B is not clearly lower than A, drop the latency half of the bullet.

Read first: `SALIKSI-MINDMAP/00 Home.md`, `20 API/api-research.md`, `30 Lib/lib-groq.md`, `30 Lib/lib-credibility.md`, `70 Issues/issues-known.md`.

## 0. What the code does today (checked 2026-11-24)

- `POST /api/research` (`saliksi/app/api/research/route.ts`) runs **sequentially**: OpenAlex (l.37) → PHILJOL (l.92, only page 1 and <5 results) → Semantic Scholar (l.156). Only PHILJOL has a timeout (5 s). OpenAlex and Semantic Scholar have none, so one slow upstream sets the p95.
- After dedupe it scores up to 10 results with `scoreCredibility` in parallel (l.214): **up to 10 Groq calls per search**. A failed score is swallowed and set to `credibility: 0` (l.221).
  → **HTTP 200 does not mean success.** Search returns 200 even when every Groq call failed. Measure success at the Groq-call level (section 3), not by status code.
- `saliksi/lib/groq.ts` failover: **3 models**, not 4 (`openai/gpt-oss-120b` → `qwen/qwen3.8-27b` → `openai/gpt-oss-20b`). It moves to the next model only when the error body says `rate_limit_exceeded` or `invalid_request_error`. Gaps:
  - A 5xx (e.g. 503 over capacity) or network error **throws immediately**, so there is no failover.
  - A 429 with a non-JSON body makes `res.json()` throw, which is also not caught as failover.
  - No backoff. If all 3 models are rate-limited at the same moment, the call fails.
  - `askGroq` and `askGroqJSON` are copy-pasted. Fix both, or merge them into one loop.

## 1. Harness (do this first, no product change)

Everything goes in `evals/latency/`. Python with `-I`, stdlib only.

1. **Query set** `queries.json`, frozen before any run: 30 queries = 15 international topics, 10 with `localSourcesOnly: true`, 5 edge cases (one word, long phrase, Filipino terms, typo, rare topic). Never swap queries after seeing results.
2. **Two servers side by side**, so slow-upstream noise hits both arms equally:
   - Baseline: `git worktree add ../saliksi-baseline <baseline-commit>` → `npm run build && npm start -p 3001`.
   - Candidate: `saliksi/` → `npm run build && npm start -p 3000`.
   - Use production builds. `npm run dev` adds compile time to the first request of each route and inflates p95.
3. **`bench.py`**: one warm-up request per server (thrown away), then 3 rounds × 30 queries. For each query, alternate baseline/candidate (ABAB, flip the order each round). Record wall time, status, article count, and the number of articles with `credibility > 0`. Write `raw/<arm>/<round>-<qid>.json`.
4. **Pacing**: every search costs about 10 Groq calls. Check the account's RPM/RPD in the Groq console first. On a free tier, wait about 20 s between searches. Real (non-injected) 429s during the latency run are a real result: log them, don't retry them away.
5. **`metrics.py`**: p50/p95 per arm with a bootstrap 95% CI (90 samples per arm; p95 from 90 samples is noisy, so report the CI). Only claim "dropped" when the CIs don't overlap.

## 2. The change (smallest set that moves p95 and reliability)

Do these in this order, and re-run section 1 after the first two to see what each one bought:

| # | Change | File | Why |
|---|---|---|---|
| 1 | Run OpenAlex and Semantic Scholar with `Promise.all`; PHILJOL still runs afterwards because it depends on the OpenAlex count | `api/research/route.ts` | Removes one serial round-trip |
| 2 | `signal: AbortSignal.timeout(6000)` on the OpenAlex and Semantic Scholar fetches | same | Caps the tail that defines p95 |
| 3 | Fail over on HTTP 429, 5xx, network error and non-JSON body (not only on the two error strings). Merge the two copy-pasted loops while you're in there | `lib/groq.ts` | Makes the failover claim true for real outages |
| 4 | If every model failed with 429, do one more pass after a short wait (honor `retry-after` when present, cap about 2 s) | `lib/groq.ts` | Covers the case where all 3 models are rate-limited at once |
| 5 | (Optional, user decides) Score all 10 results in **one** `askGroqJSON` call instead of 10 | `route.ts` + `lib/credibility.ts` | Biggest latency and rate-limit win, but it changes the scoring output, so the search score may stop matching the credibility tab. Only do it with a quick check that scores stay close |

Also: `lib/groq.ts` reads `process.env.GROQ_BASE_URL ?? "https://api.groq.com/openai/v1"`. This one line is what lets section 3 inject faults. The default leaves production behavior unchanged.

**Self-check (free, no API calls):** `saliksi/lib/groq.test.ts` with `node:test`. Stub `globalThis.fetch` and assert: (a) a 429 on model 1 returns model 2's answer; (b) a 503 fails over; (c) a non-JSON 429 fails over; (d) all-429 throws after the retry pass; (e) a 400 that isn't a model error does **not** fail over. Run it with `node --test saliksi/lib/groq.test.ts` (Node 24 strips the types; check that the import resolves).

## 3. Failover under simulated rate limits

`fault_proxy.py`: a stdlib HTTP server on `127.0.0.1:8787` that forwards `/chat/completions` to the real Groq API. Before forwarding, it reads `model` from the body and, using a seeded RNG, returns the real Groq 429 shape instead: status 429, `{"error":{"message":"Rate limit reached (injected)","type":"tokens","code":"rate_limit_exceeded"}}`. It passes the `Authorization` header through and **never logs headers or the key**. Per attempt it logs: model, injected yes/no, upstream status.

Start the candidate server with `GROQ_BASE_URL=http://127.0.0.1:8787` and run the 30 queries once per scenario:

| Scenario | Injection |
|---|---|
| S1 | primary model 30% |
| S2 | primary model 60% |
| S3 | primary model 100% (primary fully down) |
| S4 | every model 30% independently (tests chain exhaustion + retry pass) |

**Metric (exact, from the proxy log, no app change needed).** Every logical Groq call starts with one attempt on the primary model and ends with at most one 200. So:
- `logical calls` = attempts on model 1 that are not retry-pass attempts (tag retry-pass attempts with a header, or count the first pass only).
- **X% (with failover)** = 200 responses ÷ logical calls.
- **Counterfactual (no failover)** = model-1 200s ÷ logical calls, i.e. what a single-model client would have kept.
- Cross-check: articles with `credibility > 0` ÷ all articles in the bench output should be about the same as X%.

Report X per scenario next to the counterfactual. Put the headline number on the resume as one named scenario (e.g. "with 60% of primary-model calls rate-limited"), not as an average of the scenarios.

## 4. Deliverables

`evals/latency/`: `queries.json`, `bench.py`, `fault_proxy.py`, `metrics.py`, `raw/`, `metrics.json`, `REPORT.md` (A, B with CIs; X per scenario vs the counterfactual; real 429s seen; what changed, by commit). After the code changes, update vault notes `lib-groq`, `api-research`, `issues-known`, and set `updated:`.

## 5. Honesty rules for the bullet

- "3-model failover", not 4.
- "Simulated rate limits" means injected 429s. Say so if asked; the report shows the setup.
- p95 comes from N searches over 30 fixed queries on live upstream APIs, so it depends on the time of day. The side-by-side ABAB run is what makes A vs B a fair comparison.
- If change 5 (batch scoring) is skipped, most of the latency is still Groq. Then B may only beat A by the upstream-timeout gain. That is fine; report it as it is.
