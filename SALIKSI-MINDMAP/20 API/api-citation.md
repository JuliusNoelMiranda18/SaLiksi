---
type: api-route
path: "saliksi/app/api/citation/route.ts"
status: active
tags:
  - api
  - citation
aliases:
  - "/api/citation"
updated: 2026-11-22
---

# API: `/api/citation` (POST)
318 LoC.

**Input:** `{ url?, doi?, text?, fileBase64?, fileName? }`
**Does:** Metadata resolution: `fetchCrossRef` ([[ext-crossref]]) → `fetchSemanticScholar` ([[ext-semantic-scholar]]) → `fetchHtmlMeta` (scrapes citation_* meta tags) → `extractPdfText(b64)`. Then `askGroqJSON(…, 4000)` formats.
**Returns:** `{ apa, mla, chicago, … }`
**Called by:** [[page-citation]], [[page-researcher]]
