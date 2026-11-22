---
type: page
path: "saliksi/app/(dashboard)/researcher/page.tsx"
status: active
tags:
  - page
  - search
updated: 2026-11-22
---

# Page: Researcher (Search Engine) — `/researcher`
972 LoC. Landing page (`app/page.tsx` redirects here). Component `ResearchDashboard`.

## Does
- Academic search with AI query suggestions, sort (credibility/year/citations) and filter (all/local/open_access).
- Expand a result → layman summary, citation, save to library folder.
- Sensitive-keyword detection (`SENSITIVE_KEYWORDS`) shows PH mental-health hotline info.
- Persists last search in **sessionStorage `dunong_search`** (see [[data-storage-keys]]).

## Calls
- [[api-suggestions]] — typeahead suggestions
- [[api-research]] — the search itself (paginated)
- [[api-layman]] — plain-language summary
- [[api-citation]] — citation for a result

## Uses
- [[lib-libraryContext]] → `saveArticle`, `folders`
- [[lib-devModeContext]] → `startLogGroup`, `addLog`, `streamAITrace`
- [[comp-FolderPickerPopup]] — choose folder on save

Flow: [[flow-search]]
