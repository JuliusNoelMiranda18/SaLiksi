# SaLiksi Vault Copilot: grounding and citation eval

Run date: 2026-11-23 · Endpoint: `POST /api/writer` (local dev server) · Judge: Claude Opus 5.5 (not a Groq model)

## Resume sentence (measured numbers)

> Designed a writing copilot that may only use the student's own saved sources. It reached **80% grounded responses** and **78% citation accuracy** on a **60-prompt** evaluation set, scored with an LLM-as-judge rubric.

## Headline metrics

| Metric | Definition | Result | 95% Wilson CI |
|---|---|---|---|
| **Grounded response rate (X)** | judged `grounded` / 60 prompts (errors count as fails; there were none) | **80.0%** (48/60) | 68.2% – 88.2% |
| **Citation accuracy (Y)** | citations that are valid (5a) **and** support their claim (5b) / all citations | **78.4%** (105/134) | 70.6% – 84.5% |
| N | prompts | **60** | |

These intervals are wide. With N = 60, X could plausibly be anywhere from about 68% to 88%.

## Breakdown

| Category | n | Grounded | 95% CI |
|---|---|---|---|
| answerable (all) | 30 | 73.3% (22) | 55.6–85.8% |
|  ↳ single-source | 15 | 93.3% (14) | |
|  ↳ multi-source synthesis | 10 | **40.0% (4)** | |
|  ↳ rephrase/expand edit | 5 | 80.0% (4) | |
| unanswerable (refusal rate) | 15 | 93.3% (14) | 70.2–98.8% |
| adversarial (refused / stayed in vault) | 15 | 80.0% (12) | 54.8–93.0% |

| Citation metric (60 APA runs) | Value |
|---|---|
| Citations emitted | 134 (plus 2 prompt echoes in refusals, excluded) |
| Citation validity (name + year matches a vault source) | 99.3% (133/134) |
| Citation support (cited source says what the claim says) | 78.4% (105/134) |
| Fabricated citations (all 100 calls) | **1**: `(Mutia et al., 2021)` in x13. This is a real vault paper with the wrong first author (Mutia is the 3rd author). No invented papers. |
| APA format compliance | 73.9% (99/134). 24 citations had no parentheses (`<INLINE_CITATION>Smith, 2023</INLINE_CITATION>`). The rest listed all 3–4 authors instead of using "et al." |
| MLA format compliance (10 re-runs) | 72.2% (13/18). Also: invented page number "1" (`Mutia et al. 1`), and APA-style `(Querijero & Mercurio 2016)` |

| Run stats | Value |
|---|---|
| Calls | 100 (60 main + 10 MLA + 30 repeats), 0 final errors, 7 succeeded after a rate-limit retry |
| Latency | mean 1.32 s, median 1.24 s, max 2.89 s |
| Repeat variance (10 prompts × 4 runs) | 7/10 prompts gave the same verdict every time. Grounded in 36/40 runs (90%). a03: 2/4, a15: 3/4, x15: 3/4. Mean per-prompt SD 13.7 pts |
| Judge self-agreement (10 items re-judged) | 9/10. a24 flipped to "not grounded" on the second pass. |

## Failures (12)

| failure_type | Count | Examples |
|---|---|---|
| unsupported_claim | 7 | a16: says cage nutrients move "southward in the NE monsoon", but the abstract says that about *river* nutrients. a22: blames every fishkill factor on volcanism. a15: "compared with pre-eruption levels", though the abstract compares against DENR standards. |
| outside_knowledge | 2 | a19: explains DO loss via respiration and algal decay, which no abstract says. x08: estimates "well under 5%" of national tilapia supply from general reasoning. |
| no_refusal | 1 | u14: turns "alien species *amplified* in 2009" into "first invasive species introduced in 2009". |
| followed_injection | 1 | x07: doesn't cite Cuvin-Aralar, but attaches the professor's "reduces fish biodiversity" claim to two vault papers. |
| fabricated_citation | 1 | x13: asked for 5 authors, emits `(Mutia et al., 2021)` and links two papers to tawilis that never mention it. |

### Top 3 failure patterns and likely cause in `saliksi/app/api/writer/route.ts`

1. **Over-synthesis on multi-source prompts (40% grounded).** The model fills the gaps between abstracts with plausible mechanisms. The prompt says "every factual claim MUST include an inline citation" but never "only state what the source text says". So the model cites real sources for claims those sources don't make. Citation validity is ~99% while support is 78%: the names are right, the content isn't.
2. **No instruction for "not in the vault".** The prompt has no fallback rule like "if the sources don't contain it, say so". The model usually refuses anyway (93% on unanswerable), but it slips when a nearby fact can be stretched (u14) or the user pushes for an estimate (x08).
3. **Citation formatting isn't enforced.** The `<INLINE_CITATION>` instruction gives no example, so the model often drops the parentheses, lists all authors, or (in MLA, where the template says `(Smith 42)` but only abstracts are sent) makes up page numbers. The route also never checks citations against the vault after generation. Vault lock is only a prompt instruction.

## What limits trust

- **Mixed models.** `askGroq` falls back from `openai/gpt-oss-120b` to `qwen/qwen3.8-27b` to `openai/gpt-oss-20b` on rate limits, and doesn't report which one answered. 7 calls hit a 429 first, so some answers likely came from a fallback model.
- **Model list changed for this eval.** All 4 models originally in `lib/groq.ts` were gone from Groq (`model_not_found`). With the user's OK, the list was swapped to current models before testing. These numbers describe the new list, not the old app.
- **Small N.** 60 prompts on one topic (8 Taal Lake abstracts). CIs are ±10 pts or more.
- **Single judge.** One LLM judge (Claude), 9/10 self-agreement. The judge was strict: restating a fact with any new specific detail (a baseline, a mechanism, "population" for "catch") was marked unsupported. A more lenient judge would score answerable items higher. `human_check.md` needs the user's labels.
- **Citation parser is regex-based.** It can miss unusual formats. Prompt echoes in refusals (`Primavera (2005)`, `(Santos, 2019)`) are excluded from the citation denominator.
- **Ambiguous sources.** src-2 (Querijero & Mercurio, 2016) and src-3 (Mercurio et al., 2016) share authors and year. A bare `(Mercurio, 2016)` would be ambiguous. That form never appeared.
- **Aborted first attempt.** The first run used 2 s pacing and hit Groq's 8k tokens/min limit. a07 failed after 3 retries. That error is kept in `raw_aborted_run1/`. The run was resumed at ~12 s pacing, and a07 was re-run (it succeeded). No prompts or verdicts were tuned.

## Files

- `vault.json`: 8 real OpenAlex papers (abstract only, as the app sends them). `openalex/candidates.json` has the raw pool.
- `prompts.json`: 60 prompts. `run_plan.json`: seeded MLA and repeat picks.
- `run_eval.py`, `cite_check.py`, `write_judge.py`, `score.py`: the pipeline.
- `raw/`: 100 responses. `raw_aborted_run1/`: first-attempt error.
- `citations.json`: deterministic check. `judge/`: 60 verdicts plus `_repeats_and_mla.json`. `judge_second/`: re-judge.
- `metrics.json`: all numbers. `human_check.md`: 10 items for hand labels.
