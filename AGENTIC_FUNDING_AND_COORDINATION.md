# Agentic Funding and Coordination — How PaperForge Fits and Extends

This document maps PaperForge to criteria around **agents that take action** (vote, move funds, evaluate work, pay for services, coordinate) and outlines extensions—including **x402 payments** and **multi-agent coordination**—so the project clearly goes beyond dashboards and chatbots.

---

## 1. Where PaperForge Already Aligns

| Criterion | PaperForge today |
|----------|-------------------|
| **Evaluate work** | Validators are automated agents that **evaluate** miner implementations: run code in sandbox, score execution/correctness/performance, no human in the loop. |
| **Coordination** | **Multi-validator consensus**: many validator agents independently score the same miner; median/consensus decides payouts. So agents coordinate outcome via consensus. |
| **Pay for services / move value** | Bittensor subnet **rewards** (TAO) flow to miners based on scores—i.e. automated “payment” for correct implementations. Validators effectively “vote with stake” on quality. |

So we already have: **agents that evaluate work** and **multi-agent coordination** (consensus over scores). What we add below strengthens **voting**, **explicit reasoning**, **paying for services**, and **x402**.

---

## 2. Extensions to Cover “Agentic Funding and Coordination”

### 2.1 Agents that take action

- **Vote on proposals**
  - **Task / paper proposals**: Let validator (or miner) agents **vote** on which papers enter the task pool (e.g. “add paper X”, “retire task Y”). Votes could be stake-weighted or one-per-validator; outcome updates the curated task set.
  - **Funding proposals**: Optional “treasury” or task bounty pool; agents vote on allocating funds to specific tasks or bounties (e.g. “fund paper Z with N TAO”).
- **Move funds**
  - Keep current: Bittensor **moves rewards** to miners by consensus.
  - Extend: Optional **direct payouts** from a shared wallet or **bounty pool** that validator agents control (e.g. multi-sig or threshold logic keyed off consensus).
- **Evaluate work**
  - Already core: validators evaluate miner code (run, score, report). No change needed; we can **expose this as an agent API** so other systems can “ask PaperForge agents to evaluate work.”
- **Pay for services**
  - **x402 (see below)**: Agents pay for task API, compute, or “implementation as a service” via HTTP 402.
  - **Bounties**: Subnet or treasury pays for “first correct implementation” of a paper; payment triggered by validator consensus.

### 2.2 Bonus for agents that explain their reasoning

- **Structured reasoning in submissions**
  - Miners: optional field **`reasoning`** (or `rationale`) in the submission: “Why this implementation matches the paper; which equations/sections; tradeoffs.”
  - Validators: optional **reasoning** in the score report: “Why I assigned this execution/correctness/performance score; which tests failed/passed.”
- **Scoring bonus**
  - Add a small **reasoning bonus** (e.g. +5% of total score or a separate “explainability” component) when:
    - Miner provides valid, non-empty `reasoning` that references the paper (e.g. section/equation IDs).
    - Validator provides structured reasoning for its scores (stored on-chain or in a side store).
  - Makes “agents that explain their reasoning” directly reward-relevant.

### 2.3 x402 + multi-agent coordination (strongest fit)

- **What x402 is**
  - Protocol using HTTP 402 so **AI agents can pay for API/compute** autonomously: request → 402 + payment requirements → agent signs payment → retry with proof → server verifies and serves. Payments in USDC (e.g. on Base), micropayments possible.
- **Where PaperForge can use x402**
  - **Task / implementation API behind 402**
    - PaperForge **task pool API** (or “get implementation” API) returns **402 Payment Required** with amount (e.g. in USDC). External **agent clients** pay via x402 and receive task spec + reference or even **miner implementation** (code + metadata). So “pay for services” = agents paying for tasks/implementations.
  - **Validators paying for compute**
    - Validator agents that run in separate infra could **pay for sandbox runs** (e.g. “run this miner code”) via x402 instead of only using their own hardware. Enables validators to be thin coordinators that **pay for evaluation as a service**.
  - **Miners paying for task pull**
    - Miner agents **pay for** “next task” or “premium task” via x402 from the task pool. Revenue can fund bounties or subnet treasury.
- **Multi-agent coordination on top**
  - **Same as today**: Multiple validator agents score the same miner → consensus (e.g. median) → rewards. No central controller.
  - **With x402**: Multiple agents can **pay for** the same or different services (task API, compute) and still coordinate only via consensus and on-chain rewards. Adds a clear “agents pay for services” dimension on top of “agents evaluate work and coordinate.”

### 2.4 Design choices that emphasize “least tooling, most design space”

- **Minimal new primitives**
  - Voting: “proposal + agent votes → outcome” (task add/remove, bounty allocation). No full DAO stack required.
  - Reasoning: optional text/structured field + small scoring bonus.
  - x402: one or two endpoints (e.g. `GET /tasks/{id}` and `POST /evaluate`) that return 402 when payment required; agent attaches payment and retries.
- **Open design space**
  - Who votes (validators only vs. miners vs. separate “governance” agents).
  - Who holds the wallet that receives x402 payments (subnet treasury vs. task poster vs. validators).
  - How reasoning is stored and verified (on-chain hash vs. side DB vs. IPFS).

---

## 3. Summary: How PaperForge Covers the Criteria

| Criterion | Coverage |
|-----------|----------|
| **Beyond dashboards and chatbots** | Validators and miners are **agents that take action**: run code, score, move rewards; optional vote on tasks/bounties. |
| **Vote on proposals** | Extension: agent votes on task pool and/or funding proposals (stake-weighted or 1p1v). |
| **Move funds** | Today: Bittensor rewards. Extension: optional treasury/bounty pool controlled by agent consensus. |
| **Evaluate work** | Core: validator agents evaluate miner implementations in sandbox; can expose as “evaluate work” API. |
| **Pay for services** | Extension: x402 on task API and/or compute API so agents pay for tasks or evaluation. |
| **Coordinate with other agents** | Core: multi-validator consensus; extension: same consensus can govern task pool and bounties. |
| **Agents explain reasoning** | Extension: optional `reasoning` + small scoring bonus for miners and validators. |
| **x402 + multi-agent coordination** | Extension: 402 on task/eval APIs; multiple agents pay and coordinate via existing consensus. |

---

## 4. Suggested next steps (for a grant or roadmap)

1. **Reasoning**
   - Add optional `reasoning` (and optionally `rationale`) to miner submission schema and validator result; define a small **reasoning bonus** in the scoring formula and document it in the architecture.
2. **Voting**
   - Design and document a minimal **proposal + vote** flow (e.g. “add/remove task,” “allocate bounty”) and who can vote (e.g. validators only at first).
3. **x402**
   - Add one **402-enabled endpoint** (e.g. “get task + reference implementation” or “request evaluation”) and document the flow for agent clients (request → 402 → pay → retry with proof).
4. **Multi-agent narrative**
   - In README and ARCHITECTURE, explicitly call out: “Validator agents evaluate work; consensus coordinates payouts; optional x402 lets agents pay for tasks/compute; optional voting lets agents govern the task pool.”

This positions PaperForge as a project that **already does** agentic evaluation and coordination and **extends** into agentic funding (x402), voting, and explainable reasoning—fitting “agentic funding and coordination” and “x402 + multi-agent coordination” clearly.

---

## 5. What you see in the local test (agentic funding)

Run **`python run_local_test.py --full`** to see agentic funding reflected in the output:

| What appears | Agentic funding angle |
|--------------|------------------------|
| **AGENTIC FUNDING (simulated)** at top | [x402] Agent paid 0.01 USDC for task fetch; [Agents] validators = agents that evaluate work and vote. |
| **agent reasoning (miner)** per miner | Miner agents explain their reasoning (why implementation matches or fails the spec). |
| **Agent votes: Val1=eligible \| Val2=...** | Each validator agent “votes” eligible/not eligible; consensus is the median. |
| **Consensus (median)** and **[OK] Eligible** | Outcome of multi-agent coordination; determines who gets paid. |
| **AGENTIC FUNDING OUTCOME (simulated)** at end | [Payment] X TAO -> Miner (consensus approved); [Move funds] agents voted, consensus authorized payouts; [x402] task fetched after payment. |

So the demo shows: **agents evaluate work**, **agents vote** (eligible/not), **consensus authorizes payments**, **funds move** to eligible miners, and **x402-style pay-for-service** (task fetch) is simulated in the narrative.
