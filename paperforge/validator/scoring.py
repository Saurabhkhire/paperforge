"""Scoring logic for validator."""

from dataclasses import dataclass
from typing import Any

from paperforge.config import (
    CORRECTNESS_WEIGHT,
    EXECUTION_WEIGHT,
    MIN_SCORE_THRESHOLD,
    PERFORMANCE_WEIGHT,
)


@dataclass
class ValidationResult:
    """Result of validator scoring."""

    execution_score: float  # 0 or 1
    correctness_score: float  # 0.0 - 1.0 (fraction of hidden tests passing)
    performance_score: float  # 0.0 - 1.0 (match to paper metric)
    final_score: float
    eligible: bool  # final_score >= MIN_SCORE_THRESHOLD
    details: dict[str, Any] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}


def compute_score(
    execution_pass: bool,
    correctness_frac: float,
    performance_frac: float,
) -> ValidationResult:
    """
    Compute weighted final score.
    - execution_pass: 0 or 1
    - correctness_frac: 0.0-1.0 (fraction of hidden tests passing)
    - performance_frac: 0.0-1.0 (how well metric matches paper)
    """
    exec_score = 1.0 if execution_pass else 0.0
    final = (
        EXECUTION_WEIGHT * exec_score
        + CORRECTNESS_WEIGHT * correctness_frac
        + PERFORMANCE_WEIGHT * performance_frac
    )
    return ValidationResult(
        execution_score=exec_score,
        correctness_score=correctness_frac,
        performance_score=performance_frac,
        final_score=round(final, 4),
        eligible=final >= MIN_SCORE_THRESHOLD,
        details={
            "weights": {
                "execution": EXECUTION_WEIGHT,
                "correctness": CORRECTNESS_WEIGHT,
                "performance": PERFORMANCE_WEIGHT,
            },
        },
    )
