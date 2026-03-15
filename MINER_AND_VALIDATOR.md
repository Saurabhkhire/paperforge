# What the Miner Does vs What the Validator Does

This document shows the **code flow** and **responsibilities** of miners and validators, with the research paper PDF in the loop.

---

## Research paper (PDF)

Each task is tied to a **CS research paper**:

- **Source:** arXiv (e.g. `https://arxiv.org/pdf/1301.3781.pdf`).
- **Local use:** PDF can be stored in the task folder as `paper.pdf` (see [Using PDF research papers](#using-pdf-research-papers)).
- **Task spec** includes `paper_id`, `paper_pdf_url`, and optionally a local path to the PDF.

---

## What the miner does

The miner **receives a task** (paper + spec), **reads the research paper** (PDF), and **produces a submission**: one Python module that implements the requested algorithm.

### Input (task package)

The miner gets a **task spec** (e.g. from the subnet or from `tasks/<task_name>/task_spec.json`):

```json
{
  "paper_id": "1301.3781",
  "paper_pdf_url": "https://arxiv.org/pdf/1301.3781.pdf",
  "algorithm_name": "skip_gram_negative_sampling",
  "function_signature": "def train_step(center_idx, context_idx, neg_indices, W, W_prime) -> ...",
  "sample_input": "{\"center\": 0, \"context\": 1, \"neg\": [2,3,4], \"vocab_size\": 10, \"dim\": 5}",
  "sample_output": "{\"loss\": 0.5, \"W_updated\": true, \"W_prime_updated\": true}",
  "performance_target": "Loss decreases over 1000 steps..."
}
```

Plus the **paper PDF** (URL or local path, e.g. `tasks/word2vec_skipgram/paper.pdf`).

### Miner flow (conceptually)

1. **Load task** (paper_id, algorithm_name, function_signature, sample_input, sample_output, performance_target).
2. **Open the PDF** (from URL or local path) and read the relevant sections/equations.
3. **Implement** the algorithm in Python so that:
   - There is a `main(sample_input)` that returns the expected shape (e.g. a dict matching `sample_output`).
   - The core logic matches the paper (e.g. Section 3.1, Eq. 4 for Word2Vec).
4. **Self-test** with `sample_input` → compare to `sample_output`.
5. **Return a submission**: code string, requirements list, docstring, complexity note, test_output.

### Miner code (what the miner produces)

The miner **returns** a `MinerSubmission` (or equivalent dict) with at least:

- **code** – single Python module (string)
- **requirements** – list of pip package names (allowlist only)
- **docstring** – citing paper and sections
- **complexity_note** – time/space complexity
- **test_output** – miner’s own run of sample_input → sample_output

Example of **code** the miner might submit (stub for Word2Vec skip-gram):

```python
"""Skip-gram negative sampling (Mikolov et al. 2013, Eq. 4).
Paper: Efficient Estimation of Word Representations in Vector Space
Section 3.1, Eq. 4. arXiv:1301.3781
"""
import json

def main(sample_input):
    """Implement algorithm from paper; return dict matching task sample_output."""
    # sample_input is dict e.g. {"center": 0, "context": 1, "neg": [2,3,4], "vocab_size": 10, "dim": 5}
    return {"loss": 0.5, "W_updated": True, "W_prime_updated": True}

def train_step(center_idx, context_idx, neg_indices, W, W_prime):
    """Skip-gram negative sampling training step (paper Eq. 4)."""
    pass
```

So: **miner = read PDF + implement algorithm + return this module + metadata.**

---

## What the validator does

The validator **receives the miner’s submission**, runs the miner’s **code in a sandbox** (local subprocess or Docker), and **scores** it using execution, correctness, and performance. It does **not** read the PDF; it only runs code and compares outputs/metrics.

### Validator flow (step by step)

1. **Receive submission**  
   Code string + requirements + (optionally) docstring, complexity_note, test_output.

2. **Check dependencies**  
   All packages in `requirements` must be in the **allowlist** (`config.ALLOWED_DEPENDENCIES`). If not → reject (e.g. exit_code 1, no run).

3. **Prepare sandbox**  
   - Create a temp dir (or Docker container).
   - Write miner’s code as `implementation.py`.
   - Write a **test script** that imports `implementation` and calls `main(sample_input)` with the task’s `sample_input`.
   - Write `requirements.txt` from submission.

4. **Run in sandbox**  
   - Install deps: `pip install -r requirements.txt` (allowlist already checked).
   - Run the test script: `from implementation import *; result = main(sample_input); print(json.dumps({"execution_pass": True, "sample_output": ...}))`.
   - Capture stdout/stderr and exit code. Timeout (e.g. 60s) and memory limits apply.

5. **Score**
   - **Execution (25%):** Pass if exit_code == 0 and no crash/timeout.
   - **Correctness (50%):** Compare `result` to task’s `sample_output` (e.g. after normalizing to JSON). Optionally run hidden test cases later.
   - **Performance (25%):** Placeholder or run a benchmark script; compare to paper’s reported metric.

6. **Return**  
   `ValidationResult`: execution_score, correctness_score, performance_score, final_score, eligible (e.g. final_score >= 0.60).

### Validator code (where it happens)

- **Sandbox run:** `paperforge/validator/sandbox.py`  
  - `check_dependencies_allowed(requirements)`  
  - `run_in_sandbox(code, requirements, test_script, timeout)`  
  - Writes `implementation.py` + `run_tests.py` + `requirements.txt` in a temp dir, runs Python (local or Docker).

- **Harness:** `paperforge/validator/harness.py`  
  - `_build_test_script(task)` – builds the script that does `main(sample_input)` and prints one JSON line.  
  - `run_validation(submission, task, task_dir)` – calls `run_in_sandbox`, parses stdout, compares to `task.sample_output`, then calls `compute_score(...)`.

- **Scoring:** `paperforge/validator/scoring.py`  
  - `compute_score(execution_pass, correctness_frac, performance_frac)`  
  - Returns `ValidationResult` with weights 0.25 / 0.50 / 0.25.

So: **validator = sandbox run + execution check + output comparison + score.**

### Validator code locations

| Step | File | What it does |
|------|------|--------------|
| Dependency check | `validator/sandbox.py` | `check_dependencies_allowed(requirements)` → reject if not in allowlist |
| Run miner code | `validator/sandbox.py` | `run_in_sandbox(code, requirements, test_script)` → temp dir, write `implementation.py` + `run_tests.py`, `pip install`, `python run_tests.py`, return exit_code, stdout, stderr |
| Build test script | `validator/harness.py` | `_build_test_script(task)` → script that does `from implementation import *; result = main(sample_input); print(json.dumps({...}))` |
| Compare output & score | `validator/harness.py` | `run_validation(submission, task, task_dir)` → parse stdout, compare `sample_output` to task’s expected, call `compute_score(...)` |
| Weights | `validator/scoring.py` | `compute_score(execution_pass, correctness_frac, performance_frac)` → 0.25·exec + 0.50·correct + 0.25·perf, eligible if ≥ 0.60 |

---

## Using PDF research papers

- **Task spec** has `paper_pdf_url` (arXiv link). Optionally the task folder can have a local **`paper.pdf`** (e.g. after running the download script).
- **Miner** should use the PDF to implement the algorithm:
  - If a local path is provided (e.g. `tasks/word2vec_skipgram/paper.pdf`), open that file.
  - Otherwise download from `paper_pdf_url` (or use a cached path from the subnet).
- **Validator** does **not** use the PDF; it only runs the miner’s code and compares results.

**Convention:** Store the PDF in the task folder as `paper.pdf` (e.g. `tasks/word2vec_skipgram/paper.pdf`). The task spec has `paper_pdf_url`; optionally set `paper_pdf_path` to that relative path so the miner knows the local file.

To **download the sample paper** into the task folder:

```bash
pip install httpx
python scripts/download_paper.py
```

This fetches the arXiv PDF for the Word2Vec task into `tasks/word2vec_skipgram/paper.pdf`. Miners can then be given the task spec plus path `tasks/word2vec_skipgram/paper.pdf` (or `paper_pdf_url`) to read the research paper.

---

## Summary

| Role      | Uses PDF? | Input                    | Output / Action |
|----------|-----------|--------------------------|------------------|
| **Miner**    | Yes       | Task spec + paper PDF    | Python module + deps + docstring + test_output |
| **Validator**| No        | Submission + task spec   | Run code in sandbox; execution + correctness + performance → score |
