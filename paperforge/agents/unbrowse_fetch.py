"""
Optional: fetch task/paper by intent using Unbrowse (API-native browser for AI agents).

Requires Unbrowse server running (e.g. npx unbrowse setup -> http://localhost:6969).
See SOLANA_AI_AND_UNBROWSE.md and https://www.unbrowse.ai/
"""

from __future__ import annotations

import os
from typing import Any


def fetch_paper_by_intent(
    arxiv_id: str,
    intent: str | None = None,
    unbrowse_url: str | None = None,
) -> dict[str, Any] | None:
    """
    Use Unbrowse to resolve an intent like "get PDF for arXiv X" and return metadata or PDF URL.

    Args:
        arxiv_id: arXiv ID (e.g. "1301.3781").
        intent: Optional intent string; default "get PDF for arXiv {arxiv_id}".
        unbrowse_url: Unbrowse server URL; default from env UNBROWSE_URL or http://localhost:6969.

    Returns:
        Dict with e.g. pdf_url, title, or None if Unbrowse unavailable / not configured.
    """
    url = unbrowse_url or os.environ.get("UNBROWSE_URL", "http://localhost:6969")
    intent = intent or f"get PDF for arXiv {arxiv_id}"
    # TODO: call Unbrowse API (HTTP) or CLI (subprocess) and parse response
    # Example: requests.post(f"{url}/resolve", json={"intent": intent, "url": f"https://arxiv.org/abs/{arxiv_id}"})
    return None
