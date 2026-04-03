import os
import json

from groq import Groq
from dotenv import load_dotenv

from src.models import SentimentResponse
from src.guardrails import clean_json_output

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"


def analyze(text: str, context: list | None = None) -> dict:
    """
    Sends text to the Groq LLM and returns a structured sentiment analysis.

    Pipeline:
        1. Build prompt (with optional memory context)
        2. Call Groq API
        3. Clean raw output (strip markdown fences)
        4. Parse and validate JSON against SentimentResponse schema

    Args:
        text:    Cleaned, validated input text.
        context: Recent memory entries for conversational context.

    Returns:
        A dict matching SentimentResponse fields, or {"error": ..., "raw": ...} on failure.
    """
    raw = None
    context_str = json.dumps(context, indent=2) if context else "None"

    prompt = f"""You are a professional crypto market analyst with deep expertise in sentiment analysis.

Analyze the sentiment of the following text and return ONLY a valid JSON object — no extra text, no markdown.

The JSON must follow this exact schema:
{{
  "sentiment": "<BULLISH | BEARISH | NEUTRAL>",
  "confidence": <float between 0.0 and 1.0>,
  "reasoning": "<one sentence explaining the sentiment>",
  "market_insight": "<relevant market context or implication>",
  "recommended_action": "<BUY | SELL | HOLD>"
}}

Recent conversation context (last interactions):
{context_str}

Text to analyze:
{text}

Return ONLY the JSON object."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        raw = response.choices[0].message.content
        cleaned = clean_json_output(raw)
        data = json.loads(cleaned)
        return SentimentResponse(**data).dict()
    except Exception as e:
        return {"error": str(e), "raw": raw}
