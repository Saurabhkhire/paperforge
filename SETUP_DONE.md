# Setup status – what’s installed and what to do next

## Installed and ready

| Item | Status |
|------|--------|
| **Rust** | Installed (`winget install Rustlang.Rustup`). Use a new terminal or add `%USERPROFILE%\.cargo\bin` to PATH. |
| **PaperForge** | Installed (`pip install -e .`). Local tests and API work without Bittensor. |
| **Tasks** | `tasks/word2vec_skipgram/` is present with `task_spec.json`, `reference.py`, `hidden_tests.py`, `benchmark.py`. |
| **Sample paper PDF** | `tasks/word2vec_skipgram/paper.pdf` downloaded (Word2Vec, arXiv 1301.3781). |

You can run local tests now:

```powershell
cd "d:\Projects\Paper Forge\paperforge"
python run_local_test.py
python run_local_test.py --multi
```

---

## Not installed (Bittensor + wallets)

**Bittensor** did not install because the build needs the **Windows SDK** (`kernel32.lib`). The MSVC linker is present, but the “Desktop development with C++” workload (including Windows SDK) may be missing or not on PATH in the build environment.

### Option 1: Install Bittensor from Developer Command Prompt

1. Open **“Developer Command Prompt for VS 2022”** (or **“x64 Native Tools Command Prompt for VS 2022”**) from the Start menu.  
   This ensures `link.exe`, `kernel32.lib`, and other SDK paths are set.
2. In that command prompt, run:
   ```bat
   set PATH=%USERPROFILE%\.cargo\bin;%PATH%
   pip install bittensor
   ```
   Or from the repo:
   ```bat
   cd /d "d:\Projects\Paper Forge\paperforge"
   scripts\install_bittensor_dev_prompt.bat
   ```
3. If it still fails with `kernel32.lib` not found, in **Visual Studio Installer** → Modify Build Tools 2022 → enable **“Desktop development with C++”** (or add **Windows 10/11 SDK**). Then retry from the Developer Command Prompt.

### Option 2: Create miner and validator wallets (after Bittensor is installed)

From a terminal where `btcli` works:

```bat
cd /d "d:\Projects\Paper Forge\paperforge"
scripts\setup_wallets.bat
```

Or run the commands yourself:

```bat
btcli wallet new_coldkey --wallet.name miner_cold
btcli wallet new_hotkey --wallet.name miner_cold --wallet.hotkey default

btcli wallet new_coldkey --wallet.name val_cold
btcli wallet new_hotkey --wallet.name val_cold --wallet.hotkey default
```

Back up the coldkey files (e.g. under `%USERPROFILE%\.bittensor\wallets\`).

---

## Summary

- **Software:** PaperForge ✅, tasks ✅, sample PDF ✅. Bittensor ❌ (install from Developer Command Prompt; may need full C++ workload).
- **Wallets:** Create after Bittensor is installed using `scripts\setup_wallets.bat` or the `btcli` commands above.
