---
type: page
path: "saliksi/app/(dashboard)/citation/page.tsx"
status: active
tags:
  - page
  - citation
updated: 2026-11-22
---

# Page: Citation Generator — `/citation`
510 LoC. Component `CitationPage`.

- Input modes: `link` (URL/DOI) | `file` (PDF, client `extractPdfText`) | `library` (SavedArticle).
- Output: APA 7 / MLA 9 / Chicago 17 rendered in `CitationBox`.

Calls [[api-citation]]. Uses [[lib-libraryContext]], [[lib-devModeContext]].
