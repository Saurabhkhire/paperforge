# Using Solana AI and Unbrowse with PaperForge

This document describes how **Solana AI** (agent SDKs on Solana) and **Unbrowse** (API-native browser for AI agents) can be used with PaperForge for agentic funding, task discovery, and paper fetching.

---

## 1. What they are

| Tool | Purpose |
|------|--------|
| **Solana AI / Solana Agent** | SDKs (TypeScript, Python, Rust) to build AI agents that interact with Solana: wallets, tokens, DeFi, transfers. Agents can hold keys, sign transactions, move funds. |
| **Unbrowse** | API-native browser for agents: discovers and reverse-engineers APIs from websites, extracts structured data, resolves natural-language intents (e.g. "get paper X") to API calls. |

---

## 2. Unbrowse in PaperForge

### 2.1 Where it fits

- **Miners** need the task (paper PDF, spec, sample I/O). Today we load from local `tasks/` or a task API.
- **Unbrowse** lets an agent resolve intents like “get paper 1301.3781” or “get task list” from URLs (e.g. arXiv, your task pool UI) without hard‑coded scrapers.

### 2.2 Use cases

| Use case | How Unbrowse helps |
|----------|--------------------|
| **Fetch paper PDF / metadata** | Miner agent calls Unbrowse with intent e.g. “get PDF for arXiv 1301.3781” and URL (arxiv.org). Unbrowse discovers the PDF download API and returns the file or link. |
| **Discover task pool API** | If the task pool is a website, the agent uses Unbrowse to resolve “list available tasks” or “get task word2vec_skipgram” and gets structured data (e.g. JSON) from the discovered API. |
| **Reference docs / APIs** | Validator or miner can resolve “get API docs for this service” from a URL and use the extracted spec for validation or implementation. |

### 2.3 Integration options

- **Option A – CLI / subprocess**  
  Run Unbrowse CLI from Python when a miner or validator needs to fetch by intent:
  ```bash
  unbrowse resolve --intent "get PDF for arXiv 1301.3781" --url "https://arxiv.org/abs/1301.3781"
  ```
  Parse stdout (or response file) for PDF path or metadata.

- **Option B – Unbrowse server**  
  Run `unbrowse` (e.g. `npx unbrowse setup`) so a server listens (e.g. localhost:6969). PaperForge calls it via HTTP with intent + URL and gets structured JSON.

- **Option C – Agent framework**  
  Use Unbrowse as a skill/tool inside an agent framework that also runs the miner or validator logic; the agent “uses Unbrowse” to fetch papers or tasks before implementing or scoring.

### 2.4 Minimal code hook (Python)

You can add a small module that calls Unbrowse when available and falls back to the existing `scripts/download_paper.py` or task loader:

```python
# paperforge/agents/unbrowse_fetch.py (optional)
import subprocess
import json

def fetch_paper_by_intent(arxiv_id: str, unbrowse_url: str = "http://localhost:6969") -> dict | None:
    """Use Unbrowse to resolve 'get paper PDF' for arXiv ID. Returns metadata or path if available."""
    # Call Unbrowse API or CLI; parse response; return {"pdf_url": "...", "title": "..."} or None
    ...
```

---

## 3. Solana AI in PaperForge

### 3.1 Where it fits

- **Agentic funding**: Agents (validators/miners) that **move funds** or **pay for services** on Solana (e.g. bounties, task payments, validator payouts).
- **Complement to Bittensor**: Keep Bittensor for consensus and scoring; use Solana for **additional** payments, bounties, or treasury so “agents pay” and “agents move funds” are visible on Solana.

### 3.2 Use cases

| Use case | How Solana AI helps |
|----------|---------------------|
| **Bounty payments** | A Solana agent (e.g. “treasury agent”) holds a wallet; when consensus says “pay Miner X”, the agent signs and sends SOL or SPL tokens to the miner’s Solana address. |
| **Pay for task / API** | Miner or validator agent uses Solana Agent Kit to pay (e.g. SOL or USDC on Solana) for “task fetch” or “run evaluation” — analogous to x402 but on Solana. |
| **Vote on proposals** | Governance or task-curation votes recorded on-chain (e.g. Solana program); agents use Solana AI to submit votes and read results. |
| **Stake / rewards** | Optional: part of rewards or staking in SPL tokens; agents manage stakes and claim rewards via Solana AI. |

### 3.3 Integration options

- **Solana Agent Kit (Python/TS)**  
  Use the kit to create an agent that has a wallet and can:
  - Transfer SOL/SPL to miner addresses when consensus approves.
  - Pay a “task API” or “evaluation service” (if you expose one) by sending tokens to a designated address.

- **Flow**  
  1. PaperForge consensus (Bittensor) decides “Miner A gets 0.15 TAO” (or a parallel “Miner A gets 0.5 SOL”).  
  2. A **Solana agent** (running your payout logic) reads that outcome (from Bittensor or a shared DB).  
  3. The agent uses Solana AI to sign and send the corresponding SOL/SPL payment to Miner A’s Solana address.

- **Minimal code hook**  
  A separate small service or script that:
  - Listens for “consensus approved payout” events (or reads from DB/API).
  - Uses Solana Agent Kit (or Solana SDK) to transfer tokens to the right addresses.  
  PaperForge core can stay Bittensor-only; Solana is an optional **funding layer**.

---

## 4. Combined: Unbrowse + Solana AI

- **Unbrowse**: Agents **discover and fetch** tasks and papers (by intent, from the web) instead of only reading from local files or a single API.
- **Solana AI**: Agents **move funds** and **pay** on Solana (bounties, pay-for-task, pay-for-evaluation).

So you get:
- **Fetch**: “Get task/paper X” via Unbrowse (and optional x402 or Solana pay-for-service).
- **Evaluate**: Existing validators evaluate work; consensus as today.
- **Pay**: Bittensor rewards (TAO) + optional Solana payouts (SOL/SPL) via Solana AI agents.

---

## 5. What to add in the repo (optional)

1. **Unbrowse**
   - Doc: this file.
   - Optional: `paperforge/agents/unbrowse_fetch.py` that calls Unbrowse (CLI or HTTP) for “fetch paper by arXiv ID” and returns PDF path or URL; miner template can use it when Unbrowse is available.
   - Optional: `scripts/run_with_unbrowse.py` that starts Unbrowse (if installed) and runs a local test that fetches a task/paper by intent.

2. **Solana AI**
   - Doc: this file.
   - Optional: `paperforge/agents/solana_payout.py` (or a separate small service) that, given a list of (address, amount) from consensus, uses Solana Agent Kit to send SOL/SPL. No change to core validator/miner logic; call it from a “payout job” or after consensus.

3. **Local test / demo**
   - In `run_local_test.py --full`, you already show “[Payment] X TAO” and “[x402]”. You can add a line like “[Solana] Simulated: 0.05 SOL -> Miner Alpha (consensus approved)” and “[Unbrowse] Simulated: task fetched by intent 'get paper 1301.3781'” so the demo narrative includes both without requiring real Solana or Unbrowse.

---

## 6. Dependencies (if you implement)

- **Unbrowse**: Node/npx (`npx unbrowse setup`); or use their API from Python with `httpx`/`requests` if they expose HTTP.
- **Solana AI**: e.g. `solana-agent-kit` (Python) or Solana SDK + wallet logic; see [Solana Agent docs](https://docs.solana-agent.com/) and [Unbrowse](https://www.unbrowse.ai/).

---

## 7. Summary

| Component | Role in PaperForge |
|-----------|--------------------|
| **Unbrowse** | Agents fetch tasks/papers by intent from the web; discover task pool or arXiv APIs without hard‑coded scrapers. |
| **Solana AI** | Agents move funds and pay on Solana (bounties, pay-for-task, pay-for-evaluation); optional funding layer alongside Bittensor. |
| **Together** | “Agents discover (Unbrowse) → implement/validate (PaperForge) → get paid (Bittensor + optional Solana).” |

You can adopt Unbrowse first for task/paper fetch, then add Solana AI for on-chain payouts and payments, without changing the core scoring and consensus design.
