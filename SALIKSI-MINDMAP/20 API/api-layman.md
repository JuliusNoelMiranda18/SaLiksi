---
type: api-route
path: "saliksi/app/api/layman/route.ts"
status: active
tags:
  - api
  - search
aliases:
  - "/api/layman"
updated: 2026-11-22
---

# API: `/api/layman` (POST)
26 LoC.

**Input:** `{ title, abstract }`
**Does:** `askGroq(…, 200)` plain-language explanation.
**Returns:** `{ description }`
**Called by:** [[page-researcher]]
