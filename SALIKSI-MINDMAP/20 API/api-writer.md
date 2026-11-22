---
type: api-route
path: "saliksi/app/api/writer/route.ts"
status: active
tags:
  - api
  - writer
aliases:
  - "/api/writer"
updated: 2026-11-22
---

# API: `/api/writer` (POST)
111 LoC.

**Input:** `{ message, history, context: { vaultSources, folderName, citationFormat, documentContent }, action }`
**Does:** Builds vault-locked prompt (sources list) → `askGroq(…, 1024)`.
**Returns:** `{ response }` (may contain `<DOCUMENT_EDIT>` / `<INLINE_CITATION>` tags)
**Called by:** [[comp-VaultCopilot]]
