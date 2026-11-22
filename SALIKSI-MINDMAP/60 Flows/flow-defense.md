---
type: flow
status: active
tags:
  - flow
  - game
updated: 2026-11-22
---

# Flow: thesis defense game
[[page-defenders]] upload PDF → [[api-extract-pdf]] → per round: [[api-defenders-question]] (panelist role + history) → user answer → [[api-defenders-evaluate]] → `heatIncrease` reduces HP.
