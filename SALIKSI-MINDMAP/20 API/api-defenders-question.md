---
type: api-route
path: "saliksi/app/api/defenders/question/route.ts"
status: active
tags:
  - api
  - game
aliases:
  - "/api/defenders/question"
updated: 2026-11-22
---

# API: `/api/defenders/question` (POST)
32 LoC.

**Input:** `{ text, panelistRole, history }`
**Does:** `askGroq(…, 200)` panelist question.
**Returns:** `{ question }`
**Called by:** [[page-defenders]]
