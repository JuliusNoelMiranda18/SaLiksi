---
type: component
path: "saliksi/components/writer/WriterEditor.tsx"
status: active
tags:
  - component
  - writer
  - core
updated: 2026-11-22
---

# components/writer/WriterEditor.tsx
1143 LoC. Multi-page document editor (contentEditable pages, not TipTap). Props `{ notebook, folder, onBack }`.
- Toolbar: `FONT_FAMILIES`, `FONT_SIZES`, `PAPER_SIZES`, `PARA_STYLES`; header/footer content.
- **Autosave** → `editNotebook(folder.id, notebook.id, {...pages, paperSize, header, footer, citationFormat})` ([[lib-libraryContext]]).
- `vaultSources = getVaultSources(folder.id)` ([[lib-writerStorage]]).
- Ghost-text autocomplete → [[api-writer-autocomplete]].
- Export → [[lib-exportDocx]] (`exportToDocxFormat`, `exportToPDF`).
- Children: [[comp-VaultCopilot]], [[comp-CitationsPanel]], [[comp-DocumentNavigator]].
