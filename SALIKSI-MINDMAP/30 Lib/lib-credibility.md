---
type: lib
path: "saliksi/lib/credibility.ts"
status: active
tags:
  - lib
  - ai
  - credibility
updated: 2026-11-22
---

# lib/credibility.ts — shared credibility scorer
81 LoC. One rubric used by search, library PDF import and the credibility tab.

- `CREDIBILITY_QUALITATIVE_GUIDELINES` (string): peer review, accreditation/indexing (Scopus, PubMed, PHILJOL, CHED), publisher reputation. Top-tier 90–100, solid 70–89, questionable <50.
- `scoreCredibility(meta)` → `askGroqJSON(…, 200)` → `{ score 0-100, reasoning }`.

Depends on [[lib-groq]]. Used by [[api-research]], [[api-credibility]]; guidelines also embedded by [[api-pdf-info]].
