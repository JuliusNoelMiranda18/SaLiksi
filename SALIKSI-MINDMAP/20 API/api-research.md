---
type: api-route
path: "saliksi/app/api/research/route.ts"
status: active
tags:
  - api
  - search
aliases:
  - "/api/research"
updated: 2026-11-22
---

# API: `/api/research` (POST)
247 LoC.

**Input:** `{ query, localSourcesOnly, page=1 }`
**Does:** 1) [[ext-openalex]] (15/page, `filter=institutions.country_code:PH` if local) → 2) [[ext-philjol]] OAI-PMH only when `localSourcesOnly` or <5 results, page 1 → 3) [[ext-semantic-scholar]] when NOT local. Dedupe by DOI/title, cap 10, then **one [[lib-credibility]] `scoreCredibility` call per result in parallel** (≈10 Groq calls per search). Sort local-first then credibility.
**Returns:** `{ articles: [...] }` or `{ articles: [], message }`
**Called by:** [[page-researcher]]
