# Architecture Overview

## System Design

```
User Input (HTTP POST /analyze)
        │
        ▼
┌─────────────────┐
│   src/main.py   │  FastAPI app — handles routing, error responses
│   (API Layer)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ src/guardrails.py   │  validate_input() — type check, length, injection guard
│ (Guardrails Layer)  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  src/memory.py      │  memory.get() — injects last 5 interactions as context
│  (Memory Layer)     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  src/llm_client.py  │  analyze() — builds prompt, calls Groq API
│  (LLM Layer)        │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  src/guardrails.py  │  clean_json_output() — strips markdown, extracts JSON
│  (Output Cleaning)  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  src/models.py      │  SentimentResponse — Pydantic validation & schema
│  (Validation)       │
└────────┬────────────┘
         │
         ▼
  Structured JSON Response
```

---

## Module Responsibilities

| Module | Responsibility |
|---|---|
| `src/main.py` | FastAPI app, HTTP routing, error handling |
| `src/models.py` | Pydantic schema for LLM structured output |
| `src/llm_client.py` | Groq API client + `analyze()` function |
| `src/memory.py` | Sliding window conversation history |
| `src/guardrails.py` | Input validation + JSON output cleaning |

---

## Key Design Decisions

### 1. Separation of Concerns
Each module has a single responsibility. This makes testing, replacement, and extension straightforward (e.g., swapping Groq for OpenAI only touches `llm_client.py`).

### 2. Module-Level Memory Instance
`memory.py` exports a single shared `memory` instance. This gives the entire app a unified memory store across all requests without requiring dependency injection.

### 3. Two-Pass Output Cleaning
The LLM response goes through `clean_json_output()` before JSON parsing:
1. Strip markdown fences (` ```json ... ``` `)
2. Extract first `{...}` block with regex
This makes the system robust even when the LLM wraps its output in prose.

### 4. Broad Exception Handling in `analyze()`
The entire LLM call chain is wrapped in a single `try/except`. Failures (API errors, JSON errors, schema validation errors) all return a uniform `{"error": ..., "raw": ...}` dict — never crashing the server.

---

## Challenges & Solutions

| Challenge | Solution |
|---|---|
| LLM returns markdown-wrapped JSON | `clean_json_output()` strips fences with regex |
| LLM returns prose instead of JSON | Regex extracts first `{...}` block |
| Prompt injection attacks | `validate_input()` keyword detection |
| API / network failures | Broad try/except returns error dict |
| Schema mismatch from LLM | Pydantic `ValidationError` caught, returns raw output |
