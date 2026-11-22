---
type: lib
path: "saliksi/lib/idb.ts"
status: active
tags:
  - lib
  - storage
updated: 2026-11-22
---

# lib/idb.ts — IndexedDB file store
43 LoC. DB `dunong_files_db` v1, object store `files` (key = id, value = dataUrl string).
`openDb`, `saveFile(id, data)`, `getFile(id)`, `deleteFile(id)`.

Used only by [[page-library]] (dynamic `import("@/lib/idb")`) for uploaded PDFs/vault files. See [[data-storage-keys]].
