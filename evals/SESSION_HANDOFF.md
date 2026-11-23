# SaLiksi session handoff (paste this into a new chat)

Read this first. It replaces the previous conversation. Date: 2026-11-23.

## Goal
The user is applying for AI engineering internships. They want a **SaLiksi project section of 3-5 resume bullets**:
- Bullet 1: overview with the most outstanding impact and the tech used.
- Other bullets: measured metrics in XYZ format ("Accomplished X as measured by Y by doing Z"). Concise, formal, direct. Vary verbs; never repeat "Achieved".

## What exists in the repo (`/Users/jouleused/Desktop/SaLiksi`)
| Path | What it is |
|---|---|
| `SALIKSI-MINDMAP/` | Obsidian vault mapping the whole codebase (79 notes, no broken links). Start at `00 Home.md`. Guide: `MINDMAP-GUIDE.md` |
| `CLAUDE.md` | Tells agents to read the vault first, open only 2-5 notes, and update the vault after code changes |
| `BUILD_MINDMAP_PROMPT.md` | Reusable, project-agnostic brief for building a vault for any other project |
| `evals/COPILOT_EVAL.md` | Agent brief for the `/api/writer` grounding + citation test (60 prompts). **Not run yet** |
| `evals/CITATION_EVAL.md` | Agent brief for the `/api/citation` test (100 DOIs + 20 URLs). **Run** |
| `evals/citation/REPORT.md` | Results of the citation run |
| `evals/citation/IMPROVEMENT_PLAN.md` | Untracked; plan to improve the citation engine |
| `evals/citation/human_check.md` | User still needs to label these 10 items by hand |

Nothing under `saliksi/` was modified. Git: vault is committed ("add vault"); CLAUDE.md, evals and this file are not committed (user hasn't asked).

## Project facts
- Next.js 16 App Router, React 19, TypeScript, Tailwind 4, Groq LLMs. No database: localStorage `dunong_library_v2`, sessionStorage `dunong_search`, IndexedDB `dunong_files_db`.
- External APIs: OpenAlex, Semantic Scholar, PHILJOL, CrossRef, Nominatim.
- 20 real API routes (22 on disk; `/api/autocomplete` and `/api/export` unused). Use "20", not "22".
- `saliksi/lib/groq.ts` is the central LLM gateway with model fallback. **The "4-model failover" claim is unverified**: the original list was 4 models (llama-3.3-70b-versatile, mixtral-8x7b-32768, llama-3.1-8b-instant, gemma2-9b-it), but the eval report saw 3 models and uncommitted local edits. Check the file before using "4-model" on a resume.

## Citation results (from `evals/citation/REPORT.md`)
- DOI path, 100 real papers: all bibliographic fields correct in all three styles for **77%** (95% CI 67.8-84.2%). 0 of 300 citations had fabricated fields.
- Strict paper-level (every field and formatting rule correct in all three styles): 20% (CI 13.3-28.9%). Reads poorly, so lead with the 77%.
- Per-field pass: authors 89%, year 100%, title 99%, journal 100%, volume 100%, issue 98.8%, pages 96.7%, DOI 100%. Avg latency 2.72 s.
- Weak spots: 10/300 false "Accessed 2025" dates; URL path 0/20 (bot-check pages cited as papers). Omit URL results from the resume.
- Caveats: DOI truth is CrossRef, the same source the engine uses, so say "verified against CrossRef records", not "independently verified". Mixed models, single judge.

## Latest bullet wording (final for citation)
> Engineered a citation engine that turns CrossRef and web metadata into APA, MLA and Chicago references, keeping every bibliographic field correct for 77% of 100 real papers with zero fabricated fields.

Shorter alternative:
> Engineered a CrossRef-backed citation engine producing APA, MLA and Chicago references with all bibliographic fields correct for 77% of 100 real papers and zero fabricated fields.

## Still open
1. Run `evals/COPILOT_EVAL.md` (needs `GROQ_API_KEY` in `saliksi/.env.local`) to get grounded-response % and citation-accuracy % for the writing-copilot bullet.
2. Verify the Groq model list before writing the failover claim; optionally write a latency/failover test.
3. Write bullet 1 (overview) once the numbers above are final.
4. User tasks: label `evals/citation/human_check.md`; decide whether to commit vault, CLAUDE.md and evals.
5. Optional, user declined for now: a PreToolUse hook enforcing "read the vault first" and a vault drift-check script.

## Known code risks (from the vault's `70 Issues/`)
Two writers to `dunong_library_v2`; last-folder delete not persisted; type mismatch between Notebook types; up to 10 parallel scoring calls per search; dead code in `lib/storage.ts`, `lib/citations.ts`, `lib/defaultTopics.ts`, `KnowledgeGraph.tsx`.

## Citation engine causes of error (`saliksi/app/api/citation/route.ts`)
Model does all formatting with no rules; `author.slice(0,30)`; hard-coded "access date 2025"; `fetchHtmlMeta` doesn't read volume/issue/pages; no bot-wall detection.

## Working preferences
Concise and formal bullets; XYZ format; don't repeat verbs; be honest about numbers (no inflated claims); report failures plainly.
