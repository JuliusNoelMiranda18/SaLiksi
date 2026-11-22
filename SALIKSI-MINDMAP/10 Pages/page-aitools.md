---
type: page
path: "saliksi/app/(dashboard)/aitools/page.tsx"
status: active
tags:
  - page
  - ai
updated: 2026-11-22
---

# Page: AI Tools — `/aitools`
1182 LoC. Component `AIToolsPage`. Tools: `"synthesis" | "gaps" | "graph" | "contradiction"` (`TOOL_BUTTONS`).

## Sub-components (all in this file)
| Component | Line | Calls |
|---|---|---|
| `SynthesisBanner` | ~185 | [[api-synthesis]] |
| `GapsBanner` | ~257 | [[api-gaps]] |
| `GraphBanner` (canvas knowledge graph) | ~355 | [[api-graph]] |
| `ContradictionBanner` | ~561 | [[api-synthesis]] (contradiction mode + `thesisStatement`) |
| `SourceSelector` | ~774 | picks sources from library folders |

Sources come from [[lib-libraryContext]] **and** directly from [[lib-libraryStore]] `getStoredFolders()`.
Client-side PDF text via `extractPdfText` (pdfjs-dist). Logs via [[lib-devModeContext]].

Note: the knowledge graph is drawn inline here; `components/KnowledgeGraph.tsx` is empty ([[issues-dead-code]]).
