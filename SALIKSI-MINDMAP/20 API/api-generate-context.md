---
type: api-route
path: "saliksi/app/api/generate-context/route.ts"
status: active
tags:
  - api
  - topics
aliases:
  - "/api/generate-context"
updated: 2026-11-22
---

# API: `/api/generate-context` (POST)
66 LoC.

**Input:** `{ location, fields }`
**Does:** `askGroqJSON` local problems/resources for a place.
**Returns:** context JSON
**Called by:** [[comp-GenerateResearchModal]]
