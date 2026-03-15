# Real Testing on Bittensor (Testnet / Mainnet)

This guide lists **what you need** and **step-by-step** to run PaperForge on the real Bittensor network (testnet first recommended).

---

## 1. What You Need (Checklist)

### Software & environment

| Item | Purpose |
|------|--------|
| **Python 3.10+** | Run miner, validator, and harness |
| **btcli** (Bittensor CLI) | Create wallets, register, stake, query chain |
| **Docker** (optional for real) | Validator sandbox for running miner code; can use local subprocess for dev |
| **Git** | Clone repo and switch branches |

### Bittensor

| Item | Purpose |
|------|--------|
| **Network** | **Finney** = testnet (recommended first). **Mainnet** = production. |
| **Subnet (netuid)** | PaperForge subnet number once it’s created (e.g. from hackathon). You need this to register. |
| **Wallet (coldkey + hotkey)** | One pair for miner, one for validator. Coldkey holds TAO; hotkey is registered on the subnet. |
| **TAO (or test TAO)** | Registration fee for miner/validator; validators need minimum stake (e.g. 1000 TAO on mainnet; testnet may differ). |

### PaperForge-specific

| Item | Purpose |
|------|--------|
| **Task pool** | At least one task (e.g. `tasks/word2vec_skipgram/`) with `task_spec.json` and optional `paper.pdf`. |
| **Validator env** | Machine that can run the scoring harness (and Docker if you use sandbox). |

---

## 2. Prerequisites (Do First)

### 2.1 Install Bittensor and btcli

```powershell
pip install bittensor>=7.0.0
# btcli is usually included; verify:
btcli --help
```

### 2.2 Install PaperForge

```powershell
cd "d:\Projects\Paper Forge\paperforge"
pip install -e .
```

### 2.3 Choose network

- **Testnet (Finney):** use `--subtensor.network finney` (or set in config). Get test TAO from faucet/discord if needed.
- **Mainnet:** use default or `--subtensor.network mainnet`. Need real TAO.

### 2.4 Get subnet UID (netuid)

- If PaperForge is already registered as a subnet, you’ll have a **netuid** (e.g. from hackathon or subnet owner).
- If you’re the subnet owner, you need to create/register the subnet first (see Bittensor docs).
- For now, treat **netuid** as a placeholder (e.g. `52` or whatever the subnet gets). Replace `NETUID` in the steps below.

---

## 3. Wallet Setup

### 3.1 Create a wallet (miner)

```powershell
btcli wallet new_coldkey --wallet.name miner_cold
btcli wallet new_hotkey --wallet.name miner_cold --wallet.hotkey default
```

Back up the coldkey (e.g. `~/.bittensor/wallets/miner_cold/coldkey`) safely.

### 3.2 Create a wallet (validator)

```powershell
btcli wallet new_coldkey --wallet.name val_cold
btcli wallet new_hotkey --wallet.name val_cold --wallet.hotkey default
```

### 3.3 Get TAO on the wallet

- **Testnet:** Use faucet / Discord to get test TAO to the coldkey address.
- **Mainnet:** Transfer TAO to the coldkey address (for registration and, for validator, stake).

---

## 4. Register on the Subnet

### 4.1 Register miner hotkey

```powershell
btcli subnet register --netuid NETUID --wallet.name miner_cold --wallet.hotkey default --subtensor.network finney
```

Pay the registration fee when prompted. After this, the miner hotkey has a UID on the subnet.

### 4.2 Register validator hotkey

```powershell
btcli subnet register --netuid NETUID --wallet.name val_cold --wallet.hotkey default --subtensor.network finney
```

### 4.3 (Validators) Stake

Validators must meet minimum stake (e.g. 1000 TAO on mainnet). Testnet may have lower or no minimum.

```powershell
btcli wallet stake --wallet.name val_cold --wallet.hotkey default --amount 1000 --subtensor.network finney
```

Adjust `--amount` and `--subtensor.network` for your case.

---

## 5. Run Miner (Real)

### 5.1 Ensure task and paper are ready

- Task spec: `tasks/word2vec_skipgram/task_spec.json`.
- Optional: `python scripts/download_paper.py` so `tasks/word2vec_skipgram/paper.pdf` exists.

### 5.2 Run miner node

**Note:** The current `paperforge-miner` is a stub. For a real test you need a miner process that:

1. Connects to the subnet (config: netuid, network, wallet).
2. Receives the current task from the chain or from a validator (per your subnet design).
3. Implements the algorithm (using miner_template logic + PDF if needed).
4. Submits the response (code + deps + metadata) back to the chain/validator.

Example (once implemented):

```powershell
paperforge-miner --netuid NETUID --wallet.name miner_cold --wallet.hotkey default --subtensor.network finney
```

Or with a config file:

```powershell
paperforge-miner --config config_miner.yaml
```

Until the miner node is wired to the Bittensor SDK, you can only do **local** tests: `python run_local_test.py` and `python run_local_test.py --multi`.

---

## 6. Run Validator (Real)

### 6.1 Ensure scoring works locally

```powershell
python run_local_test.py
python run_local_test.py --multi
```

Confirm execution, correctness, and final score look correct.

### 6.2 Run validator node

**Note:** The current `paperforge-validator` is a stub. For a real test you need a validator process that:

1. Connects to the subnet (netuid, network, wallet).
2. Gets the current task (from local task pool or chain).
3. For each miner UID, retrieves the miner’s submission (from chain or off-chain).
4. Runs the scoring harness (sandbox or local) and gets a score.
5. Writes weights/scores to the chain so the network can compute consensus and rewards.

Example (once implemented):

```powershell
paperforge-validator --netuid NETUID --wallet.name val_cold --wallet.hotkey default --subtensor.network finney
```

Until the validator node is wired to the Bittensor SDK, real “validator” testing is limited to the local harness: `run_validation()` in `run_local_test.py`.

---

## 7. Steps Summary (Quick List)

1. **Prerequisites:** Python 3.10+, `pip install bittensor`, `pip install -e .` in PaperForge repo.
2. **Network:** Decide Finney (testnet) vs mainnet; get test TAO if Finney.
3. **Wallets:** Create coldkey + hotkey for miner and for validator; fund coldkey.
4. **Subnet:** Get **netuid** (PaperForge subnet id).
5. **Register:** `btcli subnet register` for miner and validator on that netuid.
6. **Stake (validator):** `btcli wallet stake` if required.
7. **Tasks:** At least one task in `tasks/` (e.g. word2vec_skipgram); optional `paper.pdf` via `scripts/download_paper.py`.
8. **Local test:** `python run_local_test.py` and `python run_local_test.py --multi`.
9. **Real miner/validator:** Implement and run miner and validator nodes that use the Bittensor SDK (current repo has stubs).

---

## 8. What’s Implemented vs TODO

| Component | Status | Notes |
|-----------|--------|--------|
| Task spec, loader, pool | Done | Use `tasks/word2vec_skipgram/`. |
| Miner submission schema | Done | Code, requirements, docstring, etc. |
| Validator harness (scoring) | Done | Execution, correctness, performance; local or Docker. |
| Local test (single/multi miner) | Done | `run_local_test.py`, `--multi`. |
| PDF download for task | Done | `scripts/download_paper.py`. |
| **Miner node (Bittensor)** | Stub | Needs: connect to subnet, receive task, submit response via SDK. |
| **Validator node (Bittensor)** | Stub | Needs: connect to subnet, pull submissions, run harness, set weights. |
| Subnet registration (create subnet) | — | Done by subnet owner; get netuid from there. |

For **real** on-chain testing, the next step is to implement the miner and validator nodes (in `paperforge/bittensor/miner_node.py` and `validator_node.py`) using the Bittensor SDK so they register, sync with the chain, and exchange task/response/weights. The steps above assume that once those are implemented, you’ll run them with the wallet and netuid you configured.
