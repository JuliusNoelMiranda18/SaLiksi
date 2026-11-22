---
type: api-route
path: "saliksi/app/api/generate-topics/route.ts"
status: active
tags:
  - api
  - topics
aliases:
  - "/api/generate-topics"
updated: 2026-11-22
---

# API: `/api/generate-topics` (POST)
63 LoC.

**Input:** `{ fields, location, problems, resources }`
**Does:** `askGroqJSON` location-based topics.
**Returns:** topics JSON
**Called by:** [[comp-GenerateResearchModal]]
