---
type: page
path: "saliksi/app/(dashboard)/writer/page.tsx"
status: active
tags:
  - page
  - writer
updated: 2026-11-22
---

# Page: Writer — `/writer`
`page.tsx` is 5 lines; it just renders [[comp-WriterPage]].

Query params: `folderId`, `notebookId` (set by [[page-library]]).

Tree:
- [[comp-WriterPage]] (notebook picker / studio)
  - [[comp-WriterEditor]] (paged editor, autosave, export)
    - [[comp-VaultCopilot]] → [[api-writer]]
    - [[comp-CitationsPanel]] → [[api-bibliography]]
    - [[comp-DocumentNavigator]] (outline)

Flow: [[flow-writer-copilot]]
