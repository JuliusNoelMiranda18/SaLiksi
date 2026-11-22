---
type: api-route
path: "saliksi/app/api/generate-gap-topics/route.ts"
status: active
tags:
  - api
  - topics
aliases:
  - "/api/generate-gap-topics"
updated: 2026-11-22
---

# API: `/api/generate-gap-topics` (POST)
62 LoC.

**Input:** `{ title, problem, opportunity, author }`
**Does:** `askGroqJSON` topics for a research frontier.
**Returns:** topics JSON
**Called by:** [[page-topic-generator]]
