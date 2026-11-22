---
type: flow
status: active
tags:
  - flow
  - devmode
updated: 2026-11-22
---

# Flow: Dev Mode trace
[[comp-Sidebar]] toggle → [[lib-devModeContext]] `isDevModeEnabled`. Pages call `startLogGroup` → `addLog` → `streamAITrace(operation, context)` → [[api-dev-trace]] (Groq streaming) → [[comp-DevModeOverlay]] shows it. The trace is **generated narration**, not instrumentation of the real request.
