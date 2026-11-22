---
type: api-route
path: "saliksi/app/api/pdf-info/route.ts"
status: active
tags:
  - api
  - pdf
aliases:
  - "/api/pdf-info"
updated: 2026-11-22
---

# API: `/api/pdf-info` (POST)
77 LoC.

**Input:** multipart `file` (PDF)
**Does:** `unpdf.extractText` → `askGroqJSON` metadata extraction (embeds `CREDIBILITY_QUALITATIVE_GUIDELINES` from [[lib-credibility]]).
**Returns:** `{ metadata }`
**Called by:** [[page-library]]
