# Cost Analysis

## Model

**Provider:** Groq  
**Model:** `llama-3.3-70b-versatile`  
**Inference:** Groq's custom LPU (Language Processing Unit) — significantly faster and cheaper than GPU-based inference.

---

## Groq Pricing (as of 2025)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|---|---|---|
| llama-3.3-70b-versatile | ~$0.59 | ~$0.79 |

---

## Per-Request Estimate

| Component | Tokens (approx.) |
|---|---|
| System prompt + schema | ~150 tokens |
| User text (avg tweet) | ~30 tokens |
| Memory context (5 items) | ~200 tokens |
| **Total input** | **~380 tokens** |
| LLM JSON output | ~80 tokens |

**Cost per request:**  
- Input: 380 / 1,000,000 × $0.59 ≈ **$0.000224**  
- Output: 80 / 1,000,000 × $0.79 ≈ **$0.000063**  
- **Total: ~$0.000287 per request**

---

## Monthly Cost Estimates

| Volume | Estimated Cost |
|---|---|
| 100 requests/month | ~$0.03 |
| 1,000 requests/month | ~$0.29 |
| 10,000 requests/month | ~$2.87 |
| 100,000 requests/month | ~$28.70 |

---

## Cost Optimization Strategies

1. **Low temperature (0.2)** — Reduces token variability; shorter, more direct outputs.
2. **Concise prompt** — Schema is defined once in the prompt; no repeated verbose instructions.
3. **Memory window = 5** — Context is capped at the last 5 interactions to avoid token bloat.
4. **Output cleaning** — Avoids retry loops caused by malformed output.
5. **Groq Free Tier** — For development and low-volume usage, Groq offers a generous free tier with rate limits.

---

## Notes

- Groq pricing is subject to change. Always verify at [groq.com/pricing](https://groq.com/pricing).
- For production at scale, consider batching requests or caching repeated inputs.
