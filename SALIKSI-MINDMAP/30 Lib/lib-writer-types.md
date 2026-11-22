---
type: lib
path: "saliksi/lib/writer.types.ts"
status: active
tags:
  - lib
  - types
  - writer
updated: 2026-11-22
---

# lib/writer.types.ts
65 LoC. Writer-module types: `Author`, `VaultSource`, `Notebook` (differs from libraryStore's!), `LibraryFolder`, `VaultDocSnapshot`, `CitationFormat = 'APA'|'MLA'|'Chicago'`, `CopilotMessage`, `WriterSettings`.

Used by [[comp-VaultCopilot]], [[comp-CitationsPanel]], [[comp-WriterEditor]], [[lib-groqService]], [[lib-writerStorage]].
⚠ Type mismatch with [[lib-libraryStore]] `Notebook` causes TS errors (see `saliksi/errors.txt`) — [[issues-known]].
