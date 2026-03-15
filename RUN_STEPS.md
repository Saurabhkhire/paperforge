# Run steps – what’s done and what to run

## Done

- **Rust installed** (via `winget install Rustlang.Rustup`). `cargo --version` works in a new terminal (add `%USERPROFILE%\.cargo\bin` to PATH if needed).
- **Tasks prepared:** `tasks/word2vec_skipgram/` exists with `task_spec.json`, `reference.py`, `paper.pdf`, etc.

---

## 1. Install Bittensor (do this next)

Bittensor failed to build because the **MSVC linker (`link.exe`) was not found**. Install it, then install Bittensor.

**Option A – Visual Studio Build Tools (recommended on Windows)**

1. Download [Build Tools for Visual Studio 2022](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
2. Run the installer and select the workload **“Desktop development with C++”**.
3. Install and **restart your terminal**.
4. Run:
   ```powershell
   pip install bittensor
   ```
   Or from repo: `pip install -e ".[bittensor]"`.

**Option B – Use a pre-built environment**

Use a Python environment (e.g. WSL, or a machine) where Bittensor and its Rust deps are already installed.

---

## 2. Prepare tasks (optional)

If you need to re-download the sample paper PDF:

```powershell
cd "d:\Projects\Paper Forge\paperforge"
python scripts/download_paper.py
```

(`tasks/word2vec_skipgram/paper.pdf` already exists from a previous run.)

---

## 3. Create wallets (after Bittensor is installed)

**Miner wallet**

```powershell
btcli wallet new_coldkey --wallet.name miner_cold
btcli wallet new_hotkey --wallet.name miner_cold --wallet.hotkey default
```

**Validator wallet**

```powershell
btcli wallet new_coldkey --wallet.name val_cold
btcli wallet new_hotkey --wallet.name val_cold --wallet.hotkey default
```

Back up coldkey files (e.g. under `~/.bittensor/wallets/`).

---

## 4. Register miner

Replace `NETUID` with the real PaperForge subnet id (from hackathon/subnet owner).

```powershell
btcli subnet register --netuid NETUID --wallet.name miner_cold --wallet.hotkey default --subtensor.network finney
```

You’ll need test TAO on the miner coldkey (e.g. from a Finney faucet) for the registration fee.

---

## 5. Register validator

```powershell
btcli subnet register --netuid NETUID --wallet.name val_cold --wallet.hotkey default --subtensor.network finney
```

---

## 6. Stake validator (if required)

If the subnet requires validator stake (e.g. 1000 TAO on mainnet; testnet may differ):

```powershell
btcli wallet stake --wallet.name val_cold --wallet.hotkey default --amount 1000 --subtensor.network finney
```

---

## Summary

| Step                    | Status / action                                      |
|-------------------------|------------------------------------------------------|
| Install Rust            | Done (winget install Rustlang.Rustup)               |
| Install VS Build Tools  | Pending → install C++ workload, then retry Bittensor |
| pip install bittensor   | Pending → run after Build Tools                      |
| Prepare tasks           | Done (word2vec_skipgram + paper.pdf present)        |
| Create wallets          | Run btcli commands after Bittensor install           |
| Register miner/validator| Run with real NETUID and test TAO                    |
