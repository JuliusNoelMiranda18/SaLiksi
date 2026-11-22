---
type: lib
path: "saliksi/lib/exportDocx.ts"
status: active
tags:
  - lib
  - writer
  - export
updated: 2026-11-22
---

# lib/exportDocx.ts — client-side export
258 LoC. Uses `docx` package + `html2pdf.js`.
- `exportToDocxFormat(pages, name, font='Times New Roman', size=12)` — HTML → `Paragraph[]` (`htmlToParagraphs`, `parseColor`, `parseSize`, `getFontFamily`).
- `exportToPDF(pages, name, font, size)`.
Used by [[comp-WriterEditor]]. (Server [[api-export]] is unused.)
