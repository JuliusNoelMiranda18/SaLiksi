---
type: api-route
path: "saliksi/app/api/bibliography/route.ts"
status: active
tags:
  - api
  - writer
  - citation
aliases:
  - "/api/bibliography"
updated: 2026-11-22
---

# API: `/api/bibliography` (POST)
33 LoC.

**Input:** `{ sources, format }`
**Does:** `askGroq(…, 256)` **per source**.
**Returns:** `{ entries }`
**Called by:** [[comp-CitationsPanel]]
