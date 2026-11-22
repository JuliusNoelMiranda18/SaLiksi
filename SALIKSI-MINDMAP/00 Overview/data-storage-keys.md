---
type: data
status: active
tags:
  - data
  - storage
updated: 2026-11-22
---

# Browser storage keys (all client-side)
| Where | Key | Owner | Holds |
|---|---|---|---|
| localStorage | `dunong_library_v2` | [[lib-libraryStore]], [[lib-writerStorage]] | `Folder[]` (whole library) |
| localStorage | `dunong_cited_<notebookId>` | [[comp-CitationsPanel]] | cited source IDs |
| localStorage | `dunong_data` | [[lib-storage-legacy]] (unused) | legacy |
| sessionStorage | `dunong_search` | [[page-researcher]] | last query/results/filters |
| IndexedDB | `dunong_files_db` / store `files` | [[lib-idb]] | uploaded file dataUrls |

Server keeps **nothing**. Only env var: `GROQ_API_KEY`.
