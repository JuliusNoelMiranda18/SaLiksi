---
type: api-route
path: "saliksi/app/api/credibility/route.ts"
status: active
tags:
  - api
  - credibility
aliases:
  - "/api/credibility"
updated: 2026-11-22
---

# API: `/api/credibility` (POST)
171 LoC.

**Input:** multipart `file` **or** JSON `{ text | url … }`
**Does:** `askGroqJSON(…, 1500)` returns metadata + `dimensions`; then the official score comes from [[lib-credibility]] `scoreCredibility(result.metadata)`. Grade: ≥80 A, ≥60 B, ≥40 C, …
**Returns:** credibility result with `score`, `grade`, `dimensions`
**Called by:** [[page-credibility]]
