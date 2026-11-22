---
type: api-route
path: "saliksi/app/api/writer/autocomplete/route.ts"
status: active
tags:
  - api
  - writer
aliases:
  - "/api/writer/autocomplete"
updated: 2026-11-22
---

# API: `/api/writer/autocomplete` (POST)
34 LoC.

**Input:** `{ prompt }`
**Does:** `askGroq(…, 100)` ghost-text continuation.
**Returns:** `{ suggestion }`
**Called by:** [[comp-WriterEditor]]
