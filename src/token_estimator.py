"""Token and USD cost estimation helpers."""

from src.cost_models import (
    CHARS_PER_TOKEN,
    DEFAULT_MODEL,
    PRICING_PER_MILLION_USD,
    CostEstimate,
)


def estimate_tokens(text: str) -> int:
    """
    Approximate token count from text length.

    Uses max(1, len(text) // 4) for non-empty text; empty text returns 0.
    """
    if not text:
        return 0
    return max(1, len(text) // CHARS_PER_TOKEN)


def normalize_model_name(model_name: str) -> str:
    if model_name.startswith("openai/"):
        return model_name.split("/", 1)[1]
    return model_name


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    model_name: str,
) -> CostEstimate:
    """Estimate USD cost from token counts and a model pricing table."""
    model_key = normalize_model_name(model_name)
    pricing = PRICING_PER_MILLION_USD.get(
        model_key, PRICING_PER_MILLION_USD[DEFAULT_MODEL]
    )

    input_tokens = max(0, input_tokens)
    output_tokens = max(0, output_tokens)
    total_tokens = input_tokens + output_tokens

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]

    return CostEstimate(
        model_name=model_key,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        input_cost_usd=round(input_cost, 6),
        output_cost_usd=round(output_cost, 6),
        total_cost_usd=round(input_cost + output_cost, 6),
        is_estimate=True,
    )
