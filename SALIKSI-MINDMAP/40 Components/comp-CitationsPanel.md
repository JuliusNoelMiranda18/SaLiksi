---
type: component
path: "saliksi/components/writer/CitationsPanel.tsx"
status: active
tags:
  - component
  - writer
  - citation
updated: 2026-11-22
---

# components/writer/CitationsPanel.tsx
296 LoC. Lists vault sources; "Cite" inserts `generateInlineCitation()` from [[lib-groqService]] (local, no API). Tracks cited IDs in **localStorage `dunong_cited_<notebookId>`** ([[data-storage-keys]]). "Generate bibliography" → [[api-bibliography]].
