---
type: lib
path: "saliksi/lib/libraryStore.ts"
status: active
tags:
  - lib
  - storage
  - types
updated: 2026-11-22
---

# lib/libraryStore.ts — library types + localStorage I/O
82 LoC. **Canonical data model.** Details in [[data-library-model]].

- Types: `Author`, `SavedArticle`, `NotebookPage`, `Notebook`, `VaultFile`, `Folder`.
- `STORAGE_KEY = 'dunong_library_v2'` ([[data-storage-keys]]).
- `getStoredFolders()` / `saveStoredFolders(folders)` (SSR-safe).

Used by [[lib-libraryContext]], [[lib-writerStorage]] (types), [[page-aitools]] (direct read), many pages for types.
