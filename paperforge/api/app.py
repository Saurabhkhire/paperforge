"""FastAPI app: paste arXiv ID, see task and top implementations."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from paperforge.task.pool import get_task_by_paper_id, get_task_pool

# Resolve tasks root relative to package
TASKS_ROOT = Path(__file__).resolve().parent.parent.parent / "tasks"

app = FastAPI(
    title="PaperForge API",
    description="CS research papers → working code",
    version="0.1.0",
)


@app.get("/")
async def root() -> HTMLResponse:
    """Simple demo UI."""
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>PaperForge</title></head>
    <body>
    <h1>PaperForge</h1>
    <p>Every CS algorithm, runnable. Every paper, implemented.</p>
    <h2>Task Pool</h2>
    <ul id="tasks"></ul>
    <h2>Query by arXiv ID</h2>
    <form action="/task" method="get">
      <input name="paper_id" placeholder="e.g. 1706.03762" />
      <button type="submit">Get Task</button>
    </form>
    </body>
    </html>
    """
    return HTMLResponse(html)


@app.get("/tasks")
async def list_tasks():
    """List all tasks in pool."""
    pool = get_task_pool(TASKS_ROOT)
    return [{"paper_id": t.paper_id, "algorithm_name": t.algorithm_name} for t in pool]


@app.get("/task")
async def get_task(paper_id: str):
    """Get task spec by arXiv ID."""
    spec = get_task_by_paper_id(TASKS_ROOT, paper_id)
    if spec is None:
        return {"error": f"No task for paper_id {paper_id}"}
    return spec.model_dump()


