---
type: page
path: "saliksi/app/(dashboard)/defenders/page.tsx"
status: active
tags:
  - page
  - game
updated: 2026-11-22
---

# Page: Thesis Defenders — `/defenders`
439 LoC. Component `DefendersPage`. Battle-style thesis defense simulator.

- `PANELISTS`: statistician, grammarian, methodologist (Dr. Cruz / Prof. Garcia / Dr. Santos).
- HP bars (`hpColor`), player HP out of 100; heat from evaluation (`heatIncrease`, default 15).
- Upload thesis PDF → text → panelists ask questions → user answers → evaluated.

## Calls
- [[api-extract-pdf]] — PDF → text
- [[api-defenders-question]]
- [[api-defenders-evaluate]]

Uses [[lib-libraryContext]] (folders) for picking documents.
