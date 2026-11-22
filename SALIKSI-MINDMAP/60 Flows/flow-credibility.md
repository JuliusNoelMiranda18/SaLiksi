---
type: flow
status: active
tags:
  - flow
  - credibility
updated: 2026-11-22
---

# Flow: credibility scoring
[[page-credibility]] (link / file / library) → [[api-credibility]] → `askGroqJSON` (metadata + dimensions) → [[lib-credibility]] `scoreCredibility` (official score) → grade A–F → UI gauge → optional save to folder.
Same scorer is used in search ([[api-research]]); same guidelines in PDF import ([[api-pdf-info]]).
