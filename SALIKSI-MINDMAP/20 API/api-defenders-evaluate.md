---
type: api-route
path: "saliksi/app/api/defenders/evaluate/route.ts"
status: active
tags:
  - api
  - game
aliases:
  - "/api/defenders/evaluate"
updated: 2026-11-22
---

# API: `/api/defenders/evaluate` (POST)
55 LoC.

**Input:** `{ text, panelistRole, question, answer }`
**Does:** `askGroq(…, 300)` → parsed JSON. On failure returns `{ heatIncrease: 10, reaction }`.
**Returns:** `{ heatIncrease, reaction, … }`
**Called by:** [[page-defenders]]
