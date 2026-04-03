# API Reference

## Base URL

```
http://localhost:8000
```

---

## Endpoints

### `GET /`

Health check.

**Response:**
```json
{
  "status": "ok",
  "service": "Crypto Sentiment Intelligence API",
  "version": "1.0.0"
}
```

---

### `POST /analyze`

Analyze the sentiment of a crypto-related text.

**Request Body:**
```json
{
  "text": "Bitcoin is pumping hard!"
}
```

**Success Response `200`:**
```json
{
  "sentiment": "BULLISH",
  "confidence": 0.92,
  "reasoning": "The phrase 'pumping hard' is strong positive market slang.",
  "market_insight": "Strong buy pressure, likely driven by retail FOMO.",
  "recommended_action": "BUY"
}
```

**Error Response `400`** — Invalid input (too short / injection detected):
```json
{
  "detail": "Invalid input: text is too short (minimum 5 characters)."
}
```

**Error Response `500`** — LLM or parsing failure:
```json
{
  "detail": {
    "error": "JSONDecodeError: ...",
    "raw": "<raw LLM output>"
  }
}
```

---

### `GET /memory`

Returns the current conversation memory.

**Response:**
```json
{
  "history": [
    {
      "input": "Bitcoin is pumping hard!",
      "output": { "sentiment": "BULLISH", ... }
    }
  ],
  "count": 1
}
```

---

### `DELETE /memory`

Clears all stored conversation memory.

**Response:**
```json
{
  "message": "Memory cleared successfully."
}
```

---

## Interactive Docs

FastAPI generates interactive documentation automatically:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
