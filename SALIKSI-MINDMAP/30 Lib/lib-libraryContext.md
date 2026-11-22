---
type: lib
path: "saliksi/lib/libraryContext.tsx"
status: active
tags:
  - lib
  - storage
  - react-context
  - core
updated: 2026-11-22
---

# lib/libraryContext.tsx — `LibraryProvider` / `useLibrary()` (CORE)
217 LoC. Client React context wrapping the whole dashboard ([[app-layouts]]).

- Loads folders from [[lib-libraryStore]] on mount; **auto-saves whole folder array on every change** (only if `folders.length > 0`).
- State: `folders`, `activeFolderId`.
- Actions: `addFolder`, `renameAFolder`, `deleteAFolder`, `saveArticle`, `editArticle`, `removeArticle`, `addNotebook`, `editNotebook` (bumps `updatedAt`), `removeNotebook`, `addToVault`, `removeFromVault`.
- IDs: `folder_<ts>_<rand>`, `nb_<ts>_<rand>`.

Consumers: [[page-researcher]], [[page-library]], [[page-credibility]], [[page-aitools]], [[page-citation]], [[page-defenders]], [[comp-WriterPage]], [[comp-WriterEditor]], [[comp-FolderPickerPopup]].

⚠ Deleting the last folder never persists (empty array skipped) — [[issues-known]].
