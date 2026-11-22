---
type: issues
status: active
tags:
  - issues
  - unused
updated: 2026-11-22
---

# Dead / unused code (safe-to-ignore when reading)
- [[lib-storage-legacy]] `lib/storage.ts`, [[lib-citations-legacy]] `lib/citations.ts`
- `lib/defaultTopics.ts` (empty), [[comp-KnowledgeGraph]] (empty)
- [[comp-AgentThinking]], [[comp-AnalysisLayout]], [[comp-ResultsDashboard]], [[comp-RichTextEditor]] (+ the TipTap deps only it uses)
- [[api-autocomplete]], [[api-export]] (+ `html-to-docx`, `html-docx-js`)
- [[lib-groqService]] `sendCopilotMessage`, `generateBibliographyEntry`
- Unused deps likely: `pdf-parse`, `groq-sdk`, `clsx`, `tailwind-merge` (verify before removing)
- Repo junk: `saliksi/errors.txt`, `saliksi/tsc_errors.log`, `saliksi/git_diff.txt`
