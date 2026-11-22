---
type: component
path: "saliksi/components/writer/WriterPage.tsx"
status: active
tags:
  - component
  - writer
updated: 2026-11-22
---

# components/writer/WriterPage.tsx
391 LoC. `WriterPage` wraps `WriterPageInner` in `<Suspense>` (needs `useSearchParams`).
- View `'select'` (folder/notebook studio, `StudioNotebookCard`) or `'editor'` → [[comp-WriterEditor]].
- Reads `folderId`/`notebookId` from URL. Uses [[lib-libraryContext]] (`addNotebook`, `removeNotebook`, `addFolder`, `activeFolderId`) and [[lib-writerStorage]] (`deleteNotebook`, `formatDate`, `countWords`).
Rendered by [[page-writer]].
