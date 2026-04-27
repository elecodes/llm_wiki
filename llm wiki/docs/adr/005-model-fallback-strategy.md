# ADR 005: Model Fallback Strategy for Quota Management

## Status
Accepted

## Context
The project relies on Google's Gemini API (specifically the Free Tier) for both the RAG-based query engine and the "Knowledge Absorption" feature. The Free Tier has strict rate limits (e.g., 15 requests per minute, 1,500 requests per day for Gemini 1.5 Flash). During active development or multi-user testing, these limits are easily reached, resulting in `429 Resource Exhausted` errors that degrade the user experience.

## Decision
We will implement a robust **Model Fallback Strategy** within the `QueryEngine` class. Instead of relying on a single hardcoded model, the system will maintain a prioritized list of available Gemini models and automatically rotate through them when a rate limit error is encountered.

### Priority List
1. `gemini-2.0-flash` (Primary, best performance)
2. `gemini-2.5-flash` (Secondary)
3. `gemini-flash-latest` (Alias for 1.5 Flash)
4. `gemini-2.0-flash-lite` (Lightweight fallback)
5. `gemini-flash-lite-latest` (Final fallback)

### Implementation Detail
- The `generate(prompt)` method in `scripts/lib/query.py` now encapsulates this logic.
- It catches `ResourceExhausted` (429) and `InternalServerError` (503) exceptions.
- It uses string matching on exception messages as a safety net for generic error types.
- If all models fail, it raises a consolidated error to the caller.

## Consequences
- **Pros**: 
  - Significant reduction in "Quota Exceeded" errors for the end-user.
  - Increased system resilience and perceived reliability.
  - No manual intervention needed when a specific model reaches its limit.
- **Cons**:
  - Potential variation in response quality/latency as the system falls back to "lite" models.
  - Slightly increased initial response time when retrying across models.
