---
type: api-route
path: "saliksi/app/api/synthesis/route.ts"
status: active
tags:
  - api
  - ai
aliases:
  - "/api/synthesis"
updated: 2026-11-22
---

# API: `/api/synthesis` (POST)
83 LoC.

**Input:** `{ articles (≥2), thesisStatement?, mode? }`
**Does:** `askGroqJSON` — common findings / contradictions / gaps; `mode` + `thesisStatement` drive the contradiction catcher.
**Returns:** synthesis JSON
**Called by:** [[page-aitools]] (Synthesis + Contradiction)
