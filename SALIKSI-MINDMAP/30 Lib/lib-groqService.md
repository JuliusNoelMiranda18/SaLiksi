---
type: lib
path: "saliksi/lib/groqService.ts"
status: partly-used
tags:
  - lib
  - ai
  - writer
  - legacy
updated: 2026-11-22
---

# lib/groqService.ts — legacy client-side Groq helper
203 LoC. Old "DUNONG Vault Co-pilot" implementation that took an `apiKey` argument and model `llama3-70b-8192`.

- `sendCopilotMessage(...)` — **unused** (replaced by [[api-writer]]).
- `generateInlineCitation(source, format)` — **pure function, no API**; used by [[comp-CitationsPanel]].
- `generateBibliographyEntry(...)` — imported by CitationsPanel but bibliography now goes through [[api-bibliography]].

See [[issues-dead-code]].
