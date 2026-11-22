---
type: flow
status: active
tags:
  - flow
  - search
updated: 2026-11-22
---

# Flow: search → save
1. [[page-researcher]] types query → [[api-suggestions]] (typeahead).
2. Submit → [[api-research]] → [[ext-openalex]] (+ [[ext-philjol]] / [[ext-semantic-scholar]]) → dedupe → cap 10 → [[lib-credibility]] × N → [[lib-groq]].
3. Results cached in sessionStorage `dunong_search`.
4. Expand → [[api-layman]] / [[api-citation]].
5. Save → [[comp-FolderPickerPopup]] → `saveArticle` ([[lib-libraryContext]]) → localStorage `dunong_library_v2`.
6. In parallel Dev Mode logs → [[flow-dev-mode]].
