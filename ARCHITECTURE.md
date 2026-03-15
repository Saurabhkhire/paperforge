# PaperForge Architecture

> **One-line pitch**: A decentralized network where miners implement CS research papers as working code, validators run it in sandbox, and machines score—no human judge, no LLM reviewer.

## 1. Use Case Summary

| Aspect | Description |
|--------|-------------|
| **Problem** | 80%+ of CS papers have no runnable implementation. Implementation takes 2–5 days ($1,500–5,000) per paper. |
| **Solution** | Subnet owners post papers + task specs → Miners implement → Validators execute in sandbox → Automated scoring → Best implementations rewarded |
| **Key differentiator** | Pure execution-based verification. Code either runs and passes tests, or it doesn't. |
| **Target market** | ML startups, research labs, EdTech, algorithm trading firms, open source projects |

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           PaperForge Bittensor Subnet                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  ┌──────────────┐    Task Package     ┌──────────────┐    Submission     ┌─────┐ │
│  │   Subnet     │ ──────────────────► │    Miners    │ ─────────────────►│Vali-│ │
│  │   Owner      │   paper_pdf, spec   │  (implement  │   code, deps,     │da-  │ │
│  │              │   function_sig      │   algorithm) │   test_output     │tors │ │
│  └──────────────┘                     └──────────────┘                    └──┬──┘ │
│         │                                      │                             │    │
│         │ arXiv API                            │                             │    │
│         ▼                                      │                             │    │
│  ┌──────────────┐                              │                    ┌────────▼──┐│
│  │  Task Pool   │                              │                    │  Scoring  ││
│  │  (curated    │                              │                    │  Harness  ││
│  │   papers)    │                              │                    │  (Docker) ││
│  └──────────────┘                              │                    └─────┬────┘│
│                                                │                          │      │
│                                                │                   ┌──────▼──────┐
│                                                │                   │ Bittensor   │
│                                                └──────────────────►│ Consensus   │
│                                                    Token rewards   │ (scores)    │
│                                                                     └────────────┘
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 3. Multiple Miners and Multiple Validators

In the live Bittensor subnet:

- **Multiple miners:** Many miners receive the same task (paper + spec). Each produces their own implementation and submits code. They compete for score and rewards.
- **Multiple validators:** Each validator independently runs miner submissions in a sandbox and assigns a score. Bittensor **consensus** (e.g. median of validator scores per miner) decides final scores and payouts, so one bad validator cannot alone inflate or slash a miner.

So: **many miners × many validators** → each miner is scored by several validators → consensus score → rewards.

For local testing, run `python run_local_test.py --multi` to simulate several miners and see each one’s submission and validator result.

## 4. Component Architecture

### 4.1 Task Package (Input to Miners)

```
task/
├── paper_pdf          # Full PDF from arXiv
├── paper_id           # e.g. 1706.03762
├── algorithm_name     # e.g. "multi-head attention"
├── language           # Python 3.10+ (default)
├── function_signature # Exact signature to implement
├── sample_input       # One example input
├── sample_output      # Expected output for sample_input
└── performance_target # e.g. "top-1 accuracy: 76.3%"
```

### 4.2 Miner Submission (Output from Miners)

```
submission/
├── code              # Single .py module
├── requirements.txt  # Dependencies (allowlist only)
├── docstring         # Cites paper, section, equation numbers
├── complexity_note   # Time/space complexity
└── test_output       # Miner's self-test: sample_input → sample_output
```

### 4.3 Validator Scoring Harness

```
                    ┌─────────────────────────────────────────┐
                    │         Validator Scoring Loop           │
                    ├─────────────────────────────────────────┤
  Submission ──────►│ 1. Build Docker sandbox (Python 3.10)   │
                    │    - No network, 4GB RAM, 60s timeout   │
                    ├─────────────────────────────────────────┤
                    │ 2. pip install (allowlist check)        │
                    ├─────────────────────────────────────────┤
                    │ 3. Execution test (25%)                 │
                    │    - Import + sample_input → sample_out  │
                    ├─────────────────────────────────────────┤
                    │ 4. Hidden test suite (50%)              │
                    │    - 5 hidden inputs, fraction passing   │
                    ├─────────────────────────────────────────┤
                    │ 5. Performance benchmark (25%)           │
                    │    - Key metric vs paper's reported      │
                    ├─────────────────────────────────────────┤
  Score 0.0–1.0 ◄───│ 6. Weighted sum → Bittensor consensus   │
                    └─────────────────────────────────────────┘
```

### 4.4 Scoring Formula

```
score = (0.25 × execution_pass) + (0.50 × hidden_test_frac) + (0.25 × performance_match)
```

- **Execution (25%)**: Binary pass/fail—code runs, no crash, timeout 60s
- **Correctness (50%)**: 5 hidden test cases, output tolerance
- **Performance (25%)**: Key metric within 10% of paper

**Minimum threshold**: 0.60 for token eligibility

## 4. Directory Structure

```
paperforge/
├── ARCHITECTURE.md           # This document
├── README.md
├── pyproject.toml            # Dependencies
├── requirements.txt
│
├── paperforge/
│   ├── __init__.py
│   ├── config.py             # Subnet config, weights, timeouts
│   ├── task/                 # Task spec and loading
│   │   ├── __init__.py
│   │   ├── schema.py         # Task package schema
│   │   ├── loader.py         # Load from arXiv / local cache
│   │   └── pool.py           # Task pool management
│   │
│   ├── miner/                # Miner logic
│   │   ├── __init__.py
│   │   ├── template.py       # Miner template / starter
│   │   └── submission.py     # Submission schema
│   │
│   ├── validator/            # Validator scoring
│   │   ├── __init__.py
│   │   ├── sandbox.py        # Docker sandbox runner
│   │   ├── harness.py        # Execution harness
│   │   ├── scoring.py        # Score computation
│   │   └── consensus.py      # Bittensor consensus hooks
│   │
│   ├── bittensor/            # Bittensor integration
│   │   ├── __init__.py
│   │   ├── miner_node.py     # Miner node (receives tasks, submits)
│   │   └── validator_node.py # Validator node (scores submissions)
│   │
│   └── api/                  # REST API (task query, demo UI)
│       ├── __init__.py
│       └── app.py            # FastAPI app
│
├── tasks/                    # Curated paper tasks
│   ├── word2vec_skipgram/    # Example: Word2Vec skip-gram
│   │   ├── task_spec.json
│   │   ├── reference.py      # Reference impl (hidden)
│   │   ├── hidden_tests.py
│   │   └── benchmark.py
│   ├── attention/            # Example: Multi-head attention
│   └── ...
│
├── miner_template/           # Standalone miner starter
│   ├── miner.py
│   └── requirements.txt
│
├── validator_harness/        # Standalone validator harness
│   ├── run.py
│   └── Dockerfile.sandbox
│
├── docker/
│   └── sandbox/              # Sandbox image for validation
│       └── Dockerfile
│
└── tests/
    ├── test_validator.py
    ├── test_scoring.py
    └── test_tasks.py
```

## 5. Data Flow

### 5.1 Mining Round

1. **Task selection**: Subnet selects next task from pool (round-robin or weighted).
2. **Task broadcast**: Miners receive task package via Bittensor.
3. **Implementation**: Miners implement, self-test, submit.
4. **Validation**: Each validator receives submissions, runs harness in Docker.
5. **Consensus**: Validators emit scores; Bittensor aggregates (e.g. median).
6. **Payout**: Miners above threshold receive rewards.

### 5.2 Validation Execution

```
Miner code + deps
       │
       ▼
┌─────────────────┐
│ Docker sandbox  │  ← Python 3.10, no network, 4GB, 60s
├─────────────────┤
│ pip install     │  ← Allowlist: numpy, torch, scipy, etc.
│ import module   │
│ run sample test │  → execution_score
│ run 5 hidden    │  → correctness_score
│ run benchmark   │  → performance_score
└─────────────────┘
       │
       ▼
  final_score = 0.25*exec + 0.50*corr + 0.25*perf
```

## 6. Technology Stack

| Component | Technology |
|-----------|------------|
| Subnet framework | Bittensor Python SDK |
| Paper ingestion | arXiv API, PyMuPDF |
| Validation sandbox | Docker, Python 3.10 |
| API / Demo UI | FastAPI |
| Task storage | JSON specs + local PDF cache |
| Duplicate detection | SQLite (seeded from Papers With Code) |
| GPU tasks (optional) | Basilica subnet (SN39) |

## 7. Security & Sandbox

- **Isolation**: Each submission runs in ephemeral Docker container
- **Network**: Disabled inside sandbox
- **Resources**: 4GB RAM, 60s timeout
- **Dependencies**: Allowlist only (no arbitrary pip)
- **State**: No persistence between runs

## 8. Dependencies & Sovereignty

| Dependency | Risk | Mitigation |
|------------|------|------------|
| arXiv | Low (Cornell non-profit) | Pre-cache papers |
| Python | Open source | Pinned version |
| Docker | Open source | Self-hosted images |
| Bittensor | Decentralized | Network consensus |
| PyPI | Medium | Pin + cache at round start |

## 9. Implementation Phases

| Phase | Deliverables |
|-------|--------------|
| **1. Core** | Task schema, submission schema, config |
| **2. Validator** | Docker sandbox, harness, scoring |
| **3. Miner** | Miner template, submission builder |
| **4. Tasks** | 3 paper tasks with ground truth |
| **5. Bittensor** | Miner node, validator node, consensus hooks |
| **6. Demo** | FastAPI UI, live testnet round |
