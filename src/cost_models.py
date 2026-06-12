"""Cost estimation models and pricing constants."""

from pydantic import BaseModel, Field

CHARS_PER_TOKEN = 4
DEFAULT_MODEL = "gpt-4o-mini"
BUDGET_WARNING_USD = 1.0

# USD per 1M tokens (approximate OpenAI list pricing; estimates only).
PRICING_PER_MILLION_USD: dict[str, dict[str, float]] = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
}

ESTIMATE_NOTE = (
    "Token counts and costs are estimates based on saved artifact text length "
    "(chars/4). Provider usage metadata is not required for this report."
)


class CostEstimate(BaseModel):
    model_name: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    input_cost_usd: float
    output_cost_usd: float
    total_cost_usd: float
    is_estimate: bool = True


class ArtifactCostSummary(BaseModel):
    model_name: str
    files_counted: int
    file_paths: list[str]
    input_tokens: int
    output_tokens: int
    total_tokens: int
    input_cost_usd: float
    output_cost_usd: float
    total_cost_usd: float
    is_estimate: bool = True
    notes: list[str] = Field(default_factory=list)
