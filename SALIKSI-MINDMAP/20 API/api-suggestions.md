---
type: api-route
path: "saliksi/app/api/suggestions/route.ts"
status: active
tags:
  - api
  - search
aliases:
  - "/api/suggestions"
updated: 2026-11-22
---

# API: `/api/suggestions` (POST)
27 LoC.

**Input:** `{ query }`
**Does:** [[lib-groq]] `askGroq(prompt, 300)` → list of query suggestions.
**Returns:** `{ suggestions: string[] }`
**Called by:** [[page-researcher]]
