from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.guardrails import validate_input
from src.llm_client import analyze
from src.memory import memory

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Crypto Sentiment Intelligence API",
    description=(
        "Production-ready AI assistant for crypto sentiment analysis. "
        "Powered by Groq (llama-3.3-70b-versatile) with structured outputs, "
        "memory, and guardrails."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------
class AnalyzeRequest(BaseModel):
    text: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
def root():
    """Health check."""
    return {"status": "ok", "service": "Crypto Sentiment Intelligence API", "version": "1.0.0"}


@app.post("/analyze", tags=["Sentiment"])
def analyze_endpoint(request: AnalyzeRequest):
    """
    Analyze the sentiment of a crypto-related text.

    Returns a structured JSON with:
    - sentiment (BULLISH / BEARISH / NEUTRAL)
    - confidence score
    - reasoning
    - market insight
    - recommended action (BUY / SELL / HOLD)
    """
    # Guardrails — validate & sanitize input
    try:
        clean = validate_input(request.text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Inject memory context and call LLM
    ctx = memory.get()
    result = analyze(clean, ctx)

    # Surface LLM / parsing errors as 500
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)

    # Store successful result in memory
    memory.add(clean, result)
    return result


@app.get("/memory", tags=["Memory"])
def get_memory():
    """Return the current conversation memory (last N interactions)."""
    return {"history": memory.get(), "count": len(memory.get())}


@app.delete("/memory", tags=["Memory"])
def clear_memory():
    """Clear all stored conversation memory."""
    memory.clear()
    return {"message": "Memory cleared successfully."}
