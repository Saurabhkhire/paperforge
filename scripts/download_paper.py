#!/usr/bin/env python3
"""
Download the research paper PDF for the sample task (Word2Vec, arXiv 1301.3781)
into tasks/word2vec_skipgram/paper.pdf.

Run from repo root:
  python scripts/download_paper.py
"""
import sys
from pathlib import Path

import httpx

TASK_DIR = Path(__file__).resolve().parent.parent / "tasks" / "word2vec_skipgram"
ARXIV_PDF_URL = "https://arxiv.org/pdf/1301.3781.pdf"
PDF_NAME = "paper.pdf"


def main():
    TASK_DIR.mkdir(parents=True, exist_ok=True)
    out_path = TASK_DIR / PDF_NAME
    print(f"Downloading {ARXIV_PDF_URL} -> {out_path}")
    try:
        r = httpx.get(ARXIV_PDF_URL, follow_redirects=True, timeout=30)
        r.raise_for_status()
        out_path.write_bytes(r.content)
        print(f"Saved {out_path} ({len(r.content)} bytes)")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
