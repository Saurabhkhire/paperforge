# Local testing (no Docker)

Use this to run and validate a sample research paper task on your machine without Docker.

---

## Research paper PDF

The sample task uses the **Word2Vec** paper. Download the PDF into the task folder so the miner can use it:

```powershell
pip install httpx
python scripts/download_paper.py
```

This writes `tasks/word2vec_skipgram/paper.pdf`. The miner receives the task spec and can read this PDF to implement the algorithm (see `MINER_AND_VALIDATOR.md`).

---

## Sample research paper

**Paper:** **Efficient Estimation of Word Representations in Vector Space** (Word2Vec)  
**Authors:** Mikolov et al., 2013  
**arXiv ID:** `1301.3781`  
**Link:** https://arxiv.org/abs/1301.3781  

**Task:** Implement the **skip-gram negative sampling** training step (Section 3.1, Eq. 4).  
**What the miner must provide:** A Python module with `main(sample_input)` that returns a dict with `loss`, `W_updated`, `W_prime_updated` matching the task’s sample output.

The task spec is in `tasks/word2vec_skipgram/task_spec.json`. The validator runs your code locally (subprocess, no Docker), checks execution and sample output, then reports scores.

---

## What to do

### 1. Install and prepare

```powershell
cd "d:\Projects\Paper Forge\paperforge"
pip install -e .
```

Ensure `numpy` is installed (used by the stub miner):

```powershell
pip install numpy
```

### 2. Run the local test

**Single miner (one submission, one validator run):**
```powershell
python run_local_test.py
```

**Multiple miners (simulate several miners; each is validated):**
```powershell
python run_local_test.py --multi
```
You’ll see each miner’s code and the validator result for each, plus a summary. In the real subnet, multiple validators would each score the same miner; consensus (e.g. median) would decide rewards.

Single-miner run will:

- Load the **word2vec_skipgram** task from `tasks/word2vec_skipgram/`
- Use the **stub miner** implementation in `run_local_test.py`
- Run the **validator harness locally** (no Docker): install deps, import your code, call `main(sample_input)`, compare output
- Print execution pass/fail, correctness, performance, and final score

### 3. (Optional) Run the miner template

```powershell
cd miner_template
python miner.py
```

This prints a submission dict for the same kind of task. You can plug that submission into the validator (e.g. by changing `run_local_test.py` to use the miner template’s output).

---

## What to check

| Check | Meaning |
|-------|--------|
| **Execution: PASS** | Code ran without crash; `main(sample_input)` completed. |
| **Correctness** | Validator compared your `main(...)` return value to the task’s `sample_output`. For the stub, the shape and values should match (e.g. `loss`, `W_updated`, `W_prime_updated`). |
| **Final score ≥ 0.60** | Submission is above the eligibility threshold. |
| **Eligible for rewards: True** | Same as above; would get rewards on the real subnet. |
| **No errors in stderr** | No import/runtime errors; if you see tracebacks, fix the miner code. |

If execution fails, look at **Stderr** in the output (and the traceback) to fix the miner. If execution passes but correctness is low, your returned dict doesn’t match the expected shape/values in `task_spec.json` → align your `main()` return value with `sample_output` there.

---

## Flow (no Docker)

1. **Task** is read from `tasks/word2vec_skipgram/task_spec.json`.
2. **Miner** is the stub in `run_local_test.py` (or your own code with the same interface).
3. **Validator** (local):
   - Writes miner code to a temp dir as `implementation.py`.
   - Builds a small test script that imports it, calls `main(sample_input)`, and prints a JSON line with `execution_pass` and `sample_output`.
   - Runs that script with `python` in a subprocess (no Docker).
   - Parses stdout, compares `sample_output` to the task’s expected output, and computes scores.

All of this runs on your machine; no Docker image or daemon is used.
