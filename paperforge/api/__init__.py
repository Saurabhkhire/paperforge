"""REST API for task query and demo UI."""

from .app import app


def run_api() -> None:
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
