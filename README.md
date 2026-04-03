# 🚀 Crypto Sentiment Intelligence Assistant

> Production-ready AI assistant for analyzing sentiment in crypto-related social media data using Large Language Models.

---

## 📌 Overview

This system processes crypto text and returns:

- **Sentiment** — BULLISH / BEARISH / NEUTRAL
- **Confidence score** — 0.0 → 1.0
- **Reasoning** — LLM explanation
- **Market insight** — contextual interpretation
- **Recommended action** — BUY / SELL / HOLD

---

## 🏗️ Project Structure

```
project/
├── notebook/
│   └── crypto_sentiment.ipynb     ← Interactive exploration notebook
├── src/
│   ├── main.py                    ← FastAPI app (POST /analyze)
│   ├── models.py                  ← Pydantic SentimentResponse schema
│   ├── llm_client.py              ← Groq client + analyze() function
│   ├── memory.py                  ← Sliding-window conversation memory
│   └── guardrails.py              ← Input validation + JSON cleaning
├── tests/
│   └── test_pipeline.py           ← 11 pytest test cases
├── docs/
│   ├── API.md                     ← Full API reference
│   ├── ARCHITECTURE.md            ← System design & decisions
│   └── COST_ANALYSIS.md           ← Token usage & cost estimates
├── .env.example                   ← API key template
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Create Environment

```bash
conda create -n crypto_env python=3.10
conda activate crypto_env
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

```bash
cp .env.example .env
# Edit .env and set your GROQ_API_KEY
```

Get your key at [console.groq.com/keys](https://console.groq.com/keys).

---

## ▶️ Running the API

```bash
uvicorn src.main:app --reload
```

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Example Request

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Bitcoin is pumping hard!"}'
```

### Example Response

```json
{
  "sentiment": "BULLISH",
  "confidence": 0.92,
  "reasoning": "Strong positive slang indicating upward price momentum.",
  "market_insight": "Retail FOMO likely driving the rally.",
  "recommended_action": "BUY"
}
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

11 test cases — no API key required (API calls are mocked).

---

## 🧠 Architecture

```
User Input → Guardrails → Memory Context → Groq LLM → JSON Cleaning → Pydantic Validation → Response
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for full details.

---

## 💰 Cost

~$0.0003 per request using `llama-3.3-70b-versatile` on Groq.  
See [docs/COST_ANALYSIS.md](docs/COST_ANALYSIS.md) for monthly estimates.

---

## 📚 Technical Requirements

| Requirement | Implementation |
|---|---|
| Structured Output | Pydantic `SentimentResponse` model |
| Reasoning | LLM prompt design with schema enforcement |
| Memory | Sliding-window `Memory` class (last 5 interactions) |
| Guardrails | Input validation + prompt injection detection + JSON cleaning |
| Production Patterns | FastAPI, error handling, Pydantic validation |

---

## 👨‍💻 Author

**Mohamed Yehia** — Machine Learning Engineer / Data Scientist
