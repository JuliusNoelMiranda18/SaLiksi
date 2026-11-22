---
type: api-route
path: "saliksi/app/api/graph/route.ts"
status: active
tags:
  - api
  - ai
aliases:
  - "/api/graph"
updated: 2026-11-22
---

# API: `/api/graph` (POST)
69 LoC.

**Input:** `{ articles (≥2) }`
**Does:** `askGroqJSON` — nodes (paper/concept/author/region) + edges.
**Returns:** graph JSON
**Called by:** [[page-aitools]]
