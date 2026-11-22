---
type: issues
status: active
tags:
  - issues
  - bugs
updated: 2026-11-23
---

# Known issues / risks (found while mapping, 2026-11-22)
- **Two writers to one key**: [[lib-writerStorage]] writes `dunong_library_v2` directly while [[lib-libraryContext]] holds its own copy and re-saves on every change → direct writes can be clobbered.
- **Last folder delete not persisted**: context skips saving when `folders.length === 0`.
- **Type mismatch**: `Notebook` in [[lib-libraryStore]] vs [[lib-writer-types]] (`citationFormat` optional vs required) — see `saliksi/errors.txt`.
- **Cost/latency**: each search makes up to 10 parallel Groq scoring calls ([[api-research]]); bibliography makes 1 call per source.
- **Model list** in [[api-dev-trace]] duplicates [[lib-groq]] and still lists decommissioned models ([[lib-groq]] fixed 2026-11-23); [[lib-groqService]] uses `llama3-70b-8192` (decommissioned).
- OpenAlex `mailto=` is hard-coded in [[api-research]].
- `.env.example` referenced by README does not exist in repo.
