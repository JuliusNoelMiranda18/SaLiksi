---
type: page
path: "saliksi/app/(dashboard)/credibility/page.tsx"
status: active
tags:
  - page
  - credibility
updated: 2026-11-22
---

# Page: Credibility Scorer — `/credibility`
640 LoC. Component `CredibilityPage`.

## Does
- Input modes: `link` | `file` | `library`. Client-side `extractPdfText` / `extractDocxText`.
- Shows A–F grade (`GRADE_CONFIG`, `GRADE_DESCRIPTIONS`, `GRADE_STROKE`), animated gauge, expandable `DimensionRow`s.
- Can save the analysed source into a folder (`saveArticle`) via [[comp-FolderPickerPopup]].

## Calls
- [[api-credibility]]

## Uses
[[lib-libraryContext]], [[lib-devModeContext]]. Flow: [[flow-credibility]]
