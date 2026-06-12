"""Token and cost estimation helpers for crew run artifacts."""

from pathlib import Path

from pydantic import BaseModel, Field

from src.redaction import redact_secrets

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


def read_artifact_text(path: Path) -> str:
    """Read artifact text safely; return empty string if missing."""
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def summarize_artifact_cost(
    paths: list[Path],
    model_name: str,
    secrets: list[str] | None = None,
) -> ArtifactCostSummary:
    """
    Estimate tokens and cost from saved artifact files.

    Splits total artifact tokens into input/output using a 1:3 ratio
    (prompt/context vs generated text proxy). This is an estimate only.
    """
    notes = [ESTIMATE_NOTE]
    file_paths: list[str] = []
    total_text_tokens = 0

    for path in paths:
        if not path.exists() or not path.is_file():
            notes.append(f"Skipped missing file: {path}")
            continue
        content = read_artifact_text(path)
        if secrets:
            content = redact_secrets(content, secrets=secrets)
        total_text_tokens += estimate_tokens(content)
        file_paths.append(str(path))

    if total_text_tokens == 0:
        input_tokens = 0
        output_tokens = 0
    else:
        input_tokens = total_text_tokens // 4
        output_tokens = total_text_tokens - input_tokens

    cost = estimate_cost(input_tokens, output_tokens, model_name)

    if cost.total_cost_usd >= BUDGET_WARNING_USD:
        notes.append(
            f"Budget warning: estimated cost ${cost.total_cost_usd:.4f} "
            f"exceeds ${BUDGET_WARNING_USD:.2f} threshold for analyzed artifacts."
        )

    return ArtifactCostSummary(
        model_name=cost.model_name,
        files_counted=len(file_paths),
        file_paths=file_paths,
        input_tokens=cost.input_tokens,
        output_tokens=cost.output_tokens,
        total_tokens=cost.total_tokens,
        input_cost_usd=cost.input_cost_usd,
        output_cost_usd=cost.output_cost_usd,
        total_cost_usd=cost.total_cost_usd,
        is_estimate=True,
        notes=notes,
    )


def budget_warning_message(
    estimated_cost_usd: float,
    threshold_usd: float = BUDGET_WARNING_USD,
) -> str | None:
    """Return a budget warning message if estimated cost exceeds threshold."""
    if estimated_cost_usd >= threshold_usd:
        return (
            f"Budget warning: estimated cost ${estimated_cost_usd:.4f} "
            f"meets or exceeds ${threshold_usd:.2f}."
        )
    return None
