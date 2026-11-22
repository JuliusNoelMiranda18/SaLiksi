---
type: component
path: "saliksi/components/writer/VaultCopilot.tsx"
status: active
tags:
  - component
  - writer
  - ai
updated: 2026-11-22
---

# components/writer/VaultCopilot.tsx
293 LoC. Chat panel. `QUICK_ACTIONS`: find supporting source, add inline citation, rephrase, expand, check claim, summarize.
POST [[api-writer]] with `{ message (+selected text), history, context:{ vaultSources, folderName, citationFormat, documentContent }, action:'chat' }`. Applies `<DOCUMENT_EDIT>` / `<INLINE_CITATION>` from the response. Types from [[lib-writer-types]].
