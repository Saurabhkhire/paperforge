"""Load task specs from local disk or arXiv."""

import json
from pathlib import Path

from .schema import TaskSpec


def load_task_spec(task_dir: Path) -> TaskSpec:
    """Load task spec from a task directory (tasks/<task_name>/task_spec.json).
    If paper.pdf exists in the task dir, sets paper_pdf_path so miners can use the local PDF.
    """
    task_dir = Path(task_dir)
    spec_path = task_dir / "task_spec.json"
    if not spec_path.exists():
        raise FileNotFoundError(f"Task spec not found: {spec_path}")
    data = json.loads(spec_path.read_text(encoding="utf-8"))
    spec = TaskSpec.model_validate(data)
    if spec.paper_pdf_path is None and (task_dir / "paper.pdf").exists():
        spec = spec.model_copy(update={"paper_pdf_path": str(task_dir / "paper.pdf")})
    return spec
