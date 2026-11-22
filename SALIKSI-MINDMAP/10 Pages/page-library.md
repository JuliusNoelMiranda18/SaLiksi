---
type: page
path: "saliksi/app/(dashboard)/library/page.tsx"
status: active
tags:
  - page
  - library
  - storage
updated: 2026-11-22
---

# Page: Library — `/library`
1357 LoC (largest file). Component `LibraryPage`.

## Does
- Folder CRUD (`NewFolderModal`), article list with sort (savedAt/title/credibility) via [[comp-ArticleCard]].
- Edit article metadata (`EditArticleModal`, `SearchableSelect`).
- PDF upload → `extractPdfMetadata()` → [[api-pdf-info]] → saved as article; file data saved to IndexedDB via [[lib-idb]] (`saveFile`, dynamic import).
- Notebooks (`NewNotebookModal`, `NotebookCard`) → opens Writer: `router.push('/writer?folderId=..&notebookId=..')` → [[page-writer]].
- **Vault**: attach articles / notebooks / files to a folder (`addToVault`, `LibraryPickerModal`, `VaultFileRow`). Vault feeds the Writer copilot via [[lib-writerStorage]] `getVaultSources`.

## Uses
- [[lib-libraryContext]] (saveArticle, addToVault, addNotebook, …)
- [[lib-libraryStore]] types (SavedArticle, Notebook, VaultFile, Author)
- [[lib-idb]]

Data model: [[data-library-model]]
