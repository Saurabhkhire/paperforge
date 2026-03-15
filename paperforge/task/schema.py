"""Task package schema."""

from pydantic import BaseModel, Field


class TaskSpec(BaseModel):
    """Input task package for miners."""

    paper_id: str = Field(..., description="arXiv ID (e.g. 1706.03762)")
    paper_pdf_url: str = Field(..., description="URL to PDF (e.g. https://arxiv.org/pdf/1301.3781.pdf)")
    paper_pdf_path: str | None = Field(default=None, description="Optional local path to PDF (e.g. tasks/word2vec_skipgram/paper.pdf)")
    algorithm_name: str = Field(..., description="Algorithm/component to implement")
    language: str = Field(default="python3.10", description="Target language")
    function_signature: str = Field(
        ..., description="Exact function signature to implement"
    )
    sample_input: str = Field(
        ..., description="Example input (JSON or repr)"
    )
    sample_output: str = Field(
        ..., description="Expected output for sample_input"
    )
    performance_target: str = Field(
        ..., description="Key metric from paper to match"
    )
    description: str = Field(default="", description="Additional context")
