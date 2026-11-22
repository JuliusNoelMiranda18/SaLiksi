---
type: api-route
path: "saliksi/app/api/generate-problem-topics/route.ts"
status: active
tags:
  - api
  - topics
aliases:
  - "/api/generate-problem-topics"
updated: 2026-11-22
---

# API: `/api/generate-problem-topics` (POST)
60 LoC.

**Input:** `{ title, tag, problem, opportunity }`
**Does:** `askGroqJSON` topics for a curated PH problem.
**Returns:** topics JSON
**Called by:** [[page-topic-generator]]
