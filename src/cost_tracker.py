"""Token and cost estimation helpers for crew run artifacts."""

from pathlib import Path

from src.cost_models import (
    BUDGET_WARNING_USD,
    ESTIMATE_NOTE,
    ArtifactCostSummary,
    CostEstimate,
)
from src.redaction import redact_secrets
from src.token_estimator import estimate_cost, estimate_tokens

__all__ = [
    "ArtifactCostSummary",
    "CostEstimate",
    "budget_warning_message",
    "estimate_cost",
    "estimate_tokens",
    "read_artifact_text",
    "summarize_artifact_cost",
]


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
