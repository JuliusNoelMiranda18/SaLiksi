---
type: component
path: "saliksi/components/GenerateResearchModal.tsx"
status: active
tags:
  - component
  - topics
  - map
updated: 2026-11-22
---

# components/GenerateResearchModal.tsx
656 LoC. Multi-step wizard: `FieldSelector` (`ALL_FIELDS`) → `LocationPicker` (Leaflet map, CDN marker icons) → `ContextSelector` → results.
- `geocodeLocation` / reverse geocode → [[ext-nominatim]]
- `fetchAIContext` → [[api-generate-context]]
- final → [[api-generate-topics]]
- exports `GeneratedData` type. Opened from [[page-topic-generator]] (dynamic, ssr:false).
