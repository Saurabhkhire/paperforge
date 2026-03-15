"""Task pool management."""

from pathlib import Path

from .loader import load_task_spec
from .schema import TaskSpec


def get_task_pool(tasks_root: Path) -> list[TaskSpec]:
    """Load all task specs from the tasks directory."""
    tasks_root = Path(tasks_root)
    if not tasks_root.exists():
        return []
    specs = []
    for d in tasks_root.iterdir():
        if d.is_dir() and (d / "task_spec.json").exists():
            try:
                spec = load_task_spec(d)
                specs.append(spec)
            except Exception:
                continue
    return specs


def get_task_by_paper_id(tasks_root: Path, paper_id: str) -> TaskSpec | None:
    """Get task spec by arXiv paper ID."""
    for spec in get_task_pool(tasks_root):
        if spec.paper_id == paper_id:
            return spec
    return None
