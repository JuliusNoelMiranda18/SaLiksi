---
type: lib
path: "saliksi/lib/writerStorage.ts"
status: active
tags:
  - lib
  - storage
  - writer
updated: 2026-11-22
---

# lib/writerStorage.ts — Writer helpers on the same store
196 LoC. Reads/writes **`dunong_library_v2` directly** (bypasses React context).

- `getFolders`, `getFolderById`, `getNotebookById`, `saveNotebook`, `renameNotebook`, `deleteNotebook`.
- `getVaultSources(folderId)` → `VaultSource[]`: folder articles + vault items (linked articles from other folders, linked notebooks as plain text ≤500 chars, uploaded files by name only).
- Utils: `countWords(html)`, `formatLastSaved`, `formatDate` (en-PH).

Used by [[comp-WriterEditor]] (`getVaultSources`, `countWords`, `formatLastSaved`), [[comp-WriterPage]] (`deleteNotebook`, `formatDate`, `countWords`).
Types from [[lib-writer-types]], [[lib-libraryStore]].

⚠ Writes here can be overwritten by the context's next auto-save — [[issues-known]].
