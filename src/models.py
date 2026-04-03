from pydantic import BaseModel


class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float
    reasoning: str
    market_insight: str
    recommended_action: str
