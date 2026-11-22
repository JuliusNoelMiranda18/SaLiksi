---
type: api-route
path: "saliksi/app/api/extract-pdf/route.ts"
status: active
tags:
  - api
  - pdf
aliases:
  - "/api/extract-pdf"
updated: 2026-11-22
---

# API: `/api/extract-pdf` (POST)
27 LoC.

**Input:** multipart `file`
**Does:** `unpdf.extractText` (mergePages). No AI.
**Returns:** `{ text }` / 422 if no text
**Called by:** [[page-defenders]]
