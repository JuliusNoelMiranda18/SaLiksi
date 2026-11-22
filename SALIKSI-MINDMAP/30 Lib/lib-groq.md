---
type: lib
path: "saliksi/lib/groq.ts"
status: active
tags:
  - lib
  - ai
  - core
updated: 2026-11-23
---

# lib/groq.ts — server-side LLM gateway (CORE)
110 LoC. **Every AI API route goes through this** (except [[api-dev-trace]]).

- `MODELS` cascade: `openai/gpt-oss-120b` → `qwen/qwen3.8-27b` → `openai/gpt-oss-20b` (swapped 2026-11-23; the old Llama/Mixtral/Gemma ids all returned `model_not_found`).
- `askGroq(prompt, maxTokens=500)` — temp 0.3, single user message, returns string.
- `askGroqJSON<T>(prompt, maxTokens=4000)` — temp 0.1, JSON system prompt, `response_format: json_object`, `JSON.parse`.
- Falls to next model on `rate_limit_exceeded` / `invalid_request_error` / "decommissioned".
- Needs env `GROQ_API_KEY` ([[ext-groq]]).

Used by: [[api-suggestions]], [[api-layman]], [[api-citation]], [[api-credibility]], [[api-pdf-info]], [[api-synthesis]], [[api-gaps]], [[api-graph]], [[api-generate-topics]], [[api-generate-context]], [[api-generate-problem-topics]], [[api-generate-gap-topics]], [[api-writer]], [[api-writer-autocomplete]], [[api-bibliography]], [[api-defenders-question]], [[api-defenders-evaluate]], [[api-autocomplete]], [[lib-credibility]].

⚠ [[api-dev-trace]] keeps its own model list (not updated) — see [[issues-known]].
