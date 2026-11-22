---
type: moc
status: active
tags:
  - moc
  - home
updated: 2026-11-22
---

# 🗺️ SaLiksi — Codebase Mind Map (START HERE)

Next.js 16 App Router · React 19 · TS · Tailwind 4 · Groq LLMs · **no database** (browser storage only).
App lives in `saliksi/`. ~13.9k LoC, 8 pages, 22 API routes.

## How it connects (one-screen summary)
```
Browser pages ──fetch──▶ /api/* routes ──▶ lib/groq.ts ──▶ Groq LLM
     │                        └──▶ OpenAlex / Semantic Scholar / PHILJOL / CrossRef
     └── useLibrary() ──▶ localStorage "dunong_library_v2"  (+ IndexedDB files)
```

## Maps
- Architecture: [[app-layouts]] · [[data-library-model]] · [[data-storage-keys]]
- Core files (touch with care): [[lib-groq]] · [[lib-libraryContext]] · [[lib-credibility]] · [[comp-WriterEditor]]
- Flows: [[flow-search]] · [[flow-writer-copilot]] · [[flow-credibility]] · [[flow-topics]] · [[flow-defense]] · [[flow-dev-mode]]
- Problems: [[issues-known]] · [[issues-dead-code]]
- Visual canvas: `SaLiksi Mindmap.canvas`

## Pages → API routes
| Page | Route | Calls |
|---|---|---|
| [[page-researcher]] | `/researcher` | [[api-suggestions]], [[api-research]], [[api-layman]], [[api-citation]] |
| [[page-topic-generator]] | `/topic-generator` | [[api-generate-problem-topics]], [[api-generate-gap-topics]], via [[comp-GenerateResearchModal]]: [[api-generate-context]], [[api-generate-topics]] |
| [[page-library]] | `/library` | [[api-pdf-info]] |
| [[page-writer]] | `/writer` | [[api-writer]], [[api-writer-autocomplete]], [[api-bibliography]] |
| [[page-credibility]] | `/credibility` | [[api-credibility]] |
| [[page-aitools]] | `/aitools` | [[api-synthesis]], [[api-gaps]], [[api-graph]] |
| [[page-citation]] | `/citation` | [[api-citation]] |
| [[page-defenders]] | `/defenders` | [[api-extract-pdf]], [[api-defenders-question]], [[api-defenders-evaluate]] |
| (all, Dev Mode) | — | [[api-dev-trace]] |

## Lib
[[lib-groq]] · [[lib-credibility]] · [[lib-libraryStore]] · [[lib-libraryContext]] · [[lib-writerStorage]] · [[lib-writer-types]] · [[lib-devModeContext]] · [[lib-idb]] · [[lib-exportDocx]] · [[lib-groqService]] · legacy: [[lib-storage-legacy]], [[lib-citations-legacy]]

## Components
Layout: [[comp-Sidebar]] · [[comp-DevModeOverlay]] — Shared: [[comp-FolderPickerPopup]] · [[comp-ArticleCard]] · [[comp-GenerateResearchModal]] — Writer: [[comp-WriterPage]] · [[comp-WriterEditor]] · [[comp-VaultCopilot]] · [[comp-CitationsPanel]] · [[comp-DocumentNavigator]]

## External services
[[ext-groq]] · [[ext-openalex]] · [[ext-semantic-scholar]] · [[ext-philjol]] · [[ext-crossref]] · [[ext-nominatim]]

## "I want to change X" → open these notes first
| Task | Notes |
|---|---|
| Change an AI prompt / model | the `api-*` note → [[lib-groq]] |
| Change search results | [[api-research]], [[lib-credibility]] |
| Change saved data shape | [[data-library-model]], [[lib-libraryStore]], [[lib-libraryContext]], [[lib-writerStorage]] |
| Writer / copilot | [[flow-writer-copilot]] |
| Add a new page | [[app-layouts]], [[comp-Sidebar]], [[_templates/page-template]] |
| Add an API route | [[lib-groq]], [[_templates/api-template]] |
