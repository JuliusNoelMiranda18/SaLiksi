---
type: page
path: "saliksi/app/(dashboard)/topic-generator/page.tsx"
status: active
tags:
  - page
  - topics
updated: 2026-11-22
---

# Page: Topic Generator — `/topic-generator`
999 LoC. Component `TopicGenerator`.

## Does
- Hard-coded data: `phTopics: Topic[]` (20 curated Philippine problems, line ~42) and `researchFrontiers: Frontier[]` (9 frontiers, line ~246).
- Cards → `ResearchPopup` → generate topic ideas; results in `GeneratedResultsView` / `GapResultsView`.
- "Use as topic" opens [[comp-GenerateResearchModal]] (loaded via `next/dynamic`, `ssr:false` because of Leaflet).

## Calls
- [[api-generate-problem-topics]] — for a curated PH problem
- [[api-generate-gap-topics]] — for a research frontier/gap
- (via modal) [[api-generate-context]], [[api-generate-topics]], [[ext-nominatim]]

Note: `lib/defaultTopics.ts` is **empty** — topic data lives inline in this page. See [[issues-dead-code]].
