# How to run and test PaperForge

## On Windows (no Bittensor)

This works on your machine without Docker or Bittensor.

### 1. Install

```powershell
cd "d:\Projects\Paper Forge\paperforge"
pip install -e .
pip install numpy
```

### 2. Get the sample paper (optional)

```powershell
pip install httpx
python scripts/download_paper.py
```

This puts the Word2Vec paper at `tasks/word2vec_skipgram/paper.pdf`.

### 3. Run local validation test

**One miner vs validator:**
```powershell
python run_local_test.py
```

**Several miners (good, wrong, crash) vs validator:**
```powershell
python run_local_test.py --multi
```

**Full subnet-style demo (multiple miners × multiple validators + consensus):**
```powershell
python run_local_test.py --full
```
This runs **5 miners** (two correct, two wrong output/shape, one crash) and **3 validators** per miner. Each validator scores the miner (with slight jitter to simulate different environments); the **consensus score** is the median. The output shows per-miner boxes with validator scores and a **summary table**: Miner × Validator scores → Consensus → Eligible for rewards. Only miners with consensus ≥ 0.60 get “[OK] Eligible”; the rest get “[--] Not eligible”. This matches the document use case: many miners, many validators, consensus decides payouts.

You’ll see each miner’s submission and the validator result (execution pass/fail, correctness, score). A score ≥ 0.60 means “eligible for rewards” on the real subnet.

### 4. Run the API (task pool)

```powershell
paperforge-api
```

Or:

```powershell
uvicorn paperforge.api.app:app --reload
```

Then open: **http://127.0.0.1:8000**  
- `GET /` — list tasks  
- `GET /tasks/{task_id}` — task details (e.g. `word2vec_skipgram`)  
- `GET /tasks/by_arxiv/1301.3781` — task by arXiv ID

### 5. Run the miner template

```powershell
cd miner_template
python miner.py
```

This prints a submission dict for the Word2Vec task. You can adapt this template for your own miner.

---

## Quick reference

| Goal              | Command                          |
|-------------------|----------------------------------|
| Local test (1 miner) | `python run_local_test.py`     |
| Local test (multi)   | `python run_local_test.py --multi` |
| **Full demo (multi miner × multi validator + consensus)** | `python run_local_test.py --full` |
| API server        | `paperforge-api` or `uvicorn paperforge.api.app:app --reload` |
| Miner template    | `cd miner_template && python miner.py` |
| Download sample PDF | `python scripts/download_paper.py` |

---

## With Bittensor (miner/validator on the network)

The full Bittensor stack (wallet, `btcli`, miner/validator nodes) does **not** build on native Windows (bittensor-wallet uses Unix-only APIs). Use **WSL 2** with Ubuntu:

1. Install WSL2 and Ubuntu.
2. In WSL: install Python, Rust, then `pip install -e ".[bittensor]"`.
3. Create wallets, register, and run miner/validator from WSL (see [REAL_TESTING.md](REAL_TESTING.md) and [CONFIG_AND_TEST.md](CONFIG_AND_TEST.md)).

Local testing and the API do **not** require Bittensor and work on Windows as above.
