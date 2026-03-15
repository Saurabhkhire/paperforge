"""Miner submission schema."""

from pydantic import BaseModel, Field


class MinerSubmission(BaseModel):
    """Output from miner for validator scoring."""

    paper_id: str = Field(..., description="arXiv ID")
    code: str = Field(..., description="Implementation as single Python module")
    requirements: list[str] = Field(
        default_factory=list,
        description="Dependencies (from requirements.txt)",
    )
    docstring: str = Field(
        default="",
        description="Module-level docstring citing paper/section/equations",
    )
    complexity_note: str = Field(
        default="",
        description="Time and space complexity",
    )
    test_output: str = Field(
        default="",
        description="Miner's self-test output: sample_input -> sample_output",
    )
