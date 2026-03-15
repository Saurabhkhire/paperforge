# PaperForge

> **CS research papers → working code implementations.** A Bittensor subnet where miners implement algorithms from papers and validators score by execution—no human judge, no LLM reviewer.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system design, component layout, data flow, and implementation phases.

## Quick Start

See **[RUN_AND_TEST.md](RUN_AND_TEST.md)** for full run/test steps.

```powershell
# Install (no Bittensor required for local testing)
pip install -e .
pip install numpy

# Local validation test (miner vs validator)
python run_local_test.py

# Run API (task pool, query by arXiv ID)
paperforge-api

# Miner template
cd miner_template && python miner.py
```

## Scoring

- **25%** Execution: code runs, no crash, 60s timeout
- **50%** Correctness: 5 hidden test cases
- **25%** Performance: key metric within 10% of paper

Minimum score **0.60** for token eligibility.

## Miner, validator, and PDFs

- **[MINER_AND_VALIDATOR.md](MINER_AND_VALIDATOR.md)** — What the miner does (with code), what the validator does (with code), and how **research paper PDFs** are used (miner reads PDF; validator only runs code).
- **Sample PDF:** `python scripts/download_paper.py` fetches the Word2Vec paper into `tasks/word2vec_skipgram/paper.pdf`.

## Project Layout

```
paperforge/
├── ARCHITECTURE.md           # Full architecture
├── MINER_AND_VALIDATOR.md    # Miner vs validator flow + code; PDF usage
├── paperforge/         # Core library
│   ├── task/           # Task specs, loader, pool
│   ├── miner/          # Submission schema
│   ├── validator/      # Sandbox, harness, scoring
│   ├── bittensor/      # Miner/validator nodes
│   └── api/            # FastAPI demo
├── tasks/              # Curated paper tasks
│   └── word2vec_skipgram/
├── miner_template/     # Starter miner
└── docker/sandbox/     # Validator sandbox image
```

## Installing Bittensor

Bittensor requires **Rust** (for the `bittensor-drand` dependency). If `pip install bittensor` fails with a Cargo/Rust error, see **[INSTALL.md](INSTALL.md)** for how to install Rust and optional Python 3.10/3.11. To install PaperForge with Bittensor: `pip install -e ".[bittensor]"`.

## Real testing (Bittensor network)

For testing on the real Bittensor testnet/mainnet (wallets, registration, running miner/validator nodes), see **[REAL_TESTING.md](REAL_TESTING.md)** for what you need and step-by-step instructions.

## Hackathon Deliverables

- [x] Architecture document
- [x] Validator harness (scoring logic + sandbox)
- [x] Miner template
- [x] Sample task (Word2Vec skip-gram)
- [ ] Live testnet demo (Bittensor testnet)
- [ ] 3 implemented paper tasks with ground truth
# paperforge
