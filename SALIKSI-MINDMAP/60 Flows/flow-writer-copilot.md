---
type: flow
status: active
tags:
  - flow
  - writer
updated: 2026-11-22
---

# Flow: library → writer → copilot → export
1. [[page-library]] creates notebook / adds vault items → `router.push('/writer?folderId&notebookId')`.
2. [[comp-WriterPage]] resolves notebook → [[comp-WriterEditor]].
3. Editor loads `getVaultSources(folder.id)` ([[lib-writerStorage]]) — folder articles + vault links.
4. Typing → [[api-writer-autocomplete]]. Autosave → `editNotebook` ([[lib-libraryContext]]).
5. [[comp-VaultCopilot]] → [[api-writer]] (vault-locked prompt) → apply `<DOCUMENT_EDIT>` / `<INLINE_CITATION>`.
6. [[comp-CitationsPanel]] → local inline citation; bibliography → [[api-bibliography]].
7. Export → [[lib-exportDocx]] (DOCX / PDF, client-side).
