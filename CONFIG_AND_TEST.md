# Configure, run, and test PaperForge

Use this after **Bittensor is installed** (see [Install Bittensor](#1-install-bittensor) if it isn’t yet).

---

## 1. Install Bittensor

On this machine the build fails with `kernel32.lib` not found. Do one of the following:

**Option A – Windows with full VS C++ env**

1. Install **Visual Studio 2022 Build Tools** with workload **“Desktop development with C++”** (includes Windows SDK).
2. Open **“Developer Command Prompt for VS 2022”** or **“x64 Native Tools Command Prompt for VS 2022”**.
3. Run:
   ```bat
   set PATH=%USERPROFILE%\.cargo\bin;%PATH%
   pip install bittensor
   ```
   Or from the repo: `scripts\install_bittensor_dev_prompt.bat`.

**Option B – WSL2 or Linux**

In WSL2 or a Linux VM, Rust + standard build-essential are usually enough:

```bash
pip install bittensor
```

**Option C – PaperForge without Bittensor**

You can run **local tests and the API** without Bittensor:

```powershell
pip install -e .
python run_local_test.py
python run_local_test.py --multi
```

---

## 2. What to configure

| What | Where / how |
|------|---------------------|
| **Network** | `finney` (testnet) or `mainnet`. Use `--subtensor.network finney` in btcli/run commands. |
| **Subnet (netuid)** | PaperForge subnet id from hackathon/subnet owner. Replace `NETUID` in commands below. |
| **Miner wallet** | Coldkey: `miner_cold`, hotkey: `default`. Create with `btcli wallet new_coldkey` / `new_hotkey`. |
| **Validator wallet** | Coldkey: `val_cold`, hotkey: `default`. Create with `btcli wallet new_coldkey` / `new_hotkey`. |
| **Task directory** | Default: `tasks/word2vec_skipgram/`. Set in code or env if you use a different path. |
| **TAO** | Test TAO (Finney) or real TAO (mainnet) on the coldkey for registration and, for validators, stake. |

No config file is required for the current scripts; wallets and network are passed via CLI.

---

## 3. Commands to run (in order)

### 3.1 Install PaperForge (if not done)

```powershell
cd "d:\Projects\Paper Forge\paperforge"
pip install -e .
```

### 3.2 Create wallets (after Bittensor is installed)

```bat
btcli wallet new_coldkey --wallet.name miner_cold
btcli wallet new_hotkey --wallet.name miner_cold --wallet.hotkey default

btcli wallet new_coldkey --wallet.name val_cold
btcli wallet new_hotkey --wallet.name val_cold --wallet.hotkey default
```

Or run: `scripts\setup_wallets.bat`  
Back up coldkey files (e.g. under `%USERPROFILE%\.bittensor\wallets\`).

### 3.3 Register on subnet (replace NETUID)

**Register miner:**

```bat
btcli subnet register --netuid NETUID --wallet.name miner_cold --wallet.hotkey default --subtensor.network finney
```

**Register validator:**

```bat
btcli subnet register --netuid NETUID --wallet.name val_cold --wallet.hotkey default --subtensor.network finney
```

**Stake validator (if required):**

```bat
btcli wallet stake --wallet.name val_cold --wallet.hotkey default --amount 1000 --subtensor.network finney
```

### 3.4 Run miner / validator nodes (when implemented)

Current repo has **stub** nodes. When real nodes exist:

```bat
paperforge-miner --netuid NETUID --wallet.name miner_cold --wallet.hotkey default --subtensor.network finney
```

```bat
paperforge-validator --netuid NETUID --wallet.name val_cold --wallet.hotkey default --subtensor.network finney
```

---

## 4. Commands to test

### 4.1 Local tests (no Bittensor needed)

**Single miner + validator run:**

```powershell
cd "d:\Projects\Paper Forge\paperforge"
python run_local_test.py
```

**Multiple miners:**

```powershell
python run_local_test.py --multi
```

**Check:** Execution PASS, Correctness 1.0 (or as expected), Final score ≥ 0.60, Eligible True for a correct submission.

### 4.2 API (task list and query)

```powershell
paperforge-api
```

Or:

```powershell
uvicorn paperforge.api.app:app --host 0.0.0.0 --port 8000
```

Then:

- List tasks: `http://localhost:8000/tasks`
- Get task by paper id: `http://localhost:8000/task?paper_id=1301.3781`

### 4.3 Bittensor / btcli (after Bittensor is installed)

**List wallets:**

```bat
btcli wallet list
```

**List subnet:**

```bat
btcli subnet list --subtensor.network finney
```

**Check registration:**

```bat
btcli subnet metagraph --netuid NETUID --subtensor.network finney
```

### 4.4 Miner template (dry run)

```powershell
cd miner_template
python miner.py
```

Prints a sample submission dict (no validator run).

---

## 5. Quick reference

| Goal | Command |
|------|--------|
| Install Bittensor | From **Developer Command Prompt**: `set PATH=%USERPROFILE%\.cargo\bin;%PATH%` then `pip install bittensor` |
| Install PaperForge | `pip install -e .` in repo root |
| Create wallets | `scripts\setup_wallets.bat` or btcli `new_coldkey` / `new_hotkey` |
| Register miner | `btcli subnet register --netuid NETUID --wallet.name miner_cold --wallet.hotkey default --subtensor.network finney` |
| Register validator | Same with `val_cold`. Then optionally `btcli wallet stake ...` |
| Local test (1 miner) | `python run_local_test.py` |
| Local test (multi miner) | `python run_local_test.py --multi` |
| Run API | `paperforge-api` or `uvicorn paperforge.api.app:app --port 8000` |
| List tasks | Browser or curl: `http://localhost:8000/tasks` |

---

## 6. If Bittensor won’t install on Windows

- Install **“Desktop development with C++”** (and Windows SDK) in Visual Studio Installer, then use **Developer Command Prompt** as above; or  
- Use **WSL2** or a **Linux** environment and `pip install bittensor` there; or  
- Use **local tests and API only** (no `btcli`, no on-chain): `python run_local_test.py`, `python run_local_test.py --multi`, and `paperforge-api`.
