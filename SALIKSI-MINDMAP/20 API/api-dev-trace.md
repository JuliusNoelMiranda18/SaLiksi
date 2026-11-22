---
type: api-route
path: "saliksi/app/api/dev-trace/route.ts"
status: active
tags:
  - api
  - devmode
aliases:
  - "/api/dev-trace"
updated: 2026-11-22
---

# API: `/api/dev-trace` (POST)
140 LoC.

**Input:** `{ operation, context, detailed }`
**Does:** Own copy of the 4-model list; calls [[ext-groq]] directly with streaming. Generates a *simulated* "reasoning trace" for Dev Mode — not a real trace of the other calls.
**Returns:** text stream
**Called by:** [[lib-devModeContext]] `streamAITrace`, [[comp-DevModeOverlay]] (detailed)
