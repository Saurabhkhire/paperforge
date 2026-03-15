# Installation

## Quick install (local testing only)

For running local tests (`run_local_test.py`), API, and miner template **without** Bittensor:

```powershell
cd "d:\Projects\Paper Forge\paperforge"
pip install -e .
pip install numpy
```

No Rust or Bittensor required.

---

## Install with Bittensor (for real subnet testing)

Bittensor and its dependency `bittensor-drand` require **Rust** (Cargo) to build on some systems. If `pip install bittensor` fails, follow the steps below.

### 1. Use Python 3.10 or 3.11 (recommended for Bittensor)

Bittensor and some dependencies have better wheel support on Python 3.10/3.11. If you're on Python 3.12+ or 3.14, consider using a venv with 3.10 or 3.11:

```powershell
# Example: create venv with Python 3.11 if installed
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[bittensor]"
```

### 2. Install Rust (required for bittensor-drand)

When `pip install bittensor` fails with **"Cargo, the Rust package manager, is not installed or is not on PATH"**:

1. **Install Rust:** https://rustup.rs/  
   - On Windows: run `winget install Rustlang.Rustup` or download `rustup-init.exe`, then follow the prompts.
2. **Restart your terminal** so `cargo` and `rustc` are on PATH.
3. Verify: `cargo --version` and `rustc --version`.

### 2b. Windows: Fix kernel32.lib (linker) and optionally OpenSSL

When the build fails with **"cannot open input file 'kernel32.lib'"** (LNK1181):

The Windows SDK is installed but `LIB` isn’t set when you run `pip` from a normal prompt. Use the helper script so the linker can find the SDK:

```bat
set PATH=%USERPROFILE%\.cargo\bin;%PATH%
scripts\install_bittensor_with_sdk.bat
```

That script sets `LIB` to your Windows Kits path (e.g. `...\Windows Kits\10\Lib\10.0.18362.0\um\x64`) and runs `pip install bittensor`. Run it from the repo root.

If you prefer to use the Developer environment only:

1. Open **"Developer Command Prompt for VS 2022"** (Start menu).
2. `cd` to the repo, then: `set PATH=%USERPROFILE%\.cargo\bin;%PATH%` and `pip install bittensor`.

When the build fails with **"Could not find directory of OpenSSL installation"** (bittensor-wallet):

`bittensor-wallet` needs OpenSSL **development** files (headers and libs), not just the runtime.

1. **Install OpenSSL for Windows** (choose one):
   - **Recommended:** [Win64 OpenSSL at slproweb.com](https://slproweb.com/products/Win32OpenSSL.html) — download **Win64 OpenSSL v3.x** (full, not “Light”) so `lib` and `include` are present. Use default install path.
   - Or install via vcpkg and set `VCPKG_ROOT`: `vcpkg install openssl:x64-windows-static-md`.
2. **Set OPENSSL_DIR** to the OpenSSL root (must contain `lib` and `include`), then run the install again:
   ```bat
   set OPENSSL_DIR=C:\Program Files\OpenSSL-Win64
   scripts\install_bittensor_with_sdk.bat
   ```
   Adjust the path if you installed elsewhere (e.g. `C:\Program Files (x86)\OpenSSL-Win64`).

### 2c. Windows: Bittensor and WSL2

Even with OpenSSL and the Windows SDK set, **bittensor-wallet** fails to build on Windows because it uses Unix-only APIs (`std::os::unix`, file descriptors, etc.). Bittensor does not provide Windows wheels for the wallet.

To run the full Bittensor stack (miner, validator, `btcli`):

1. **Use WSL 2** with Ubuntu: [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install).
2. Inside WSL (Ubuntu), install Python, Rust, and dependencies, then:
   ```bash
   pip install -e ".[bittensor]"
   # or: pip install bittensor
   ```
3. Run miners/validators and `btcli` from the WSL environment.

On native Windows you can still run **local testing** (no Bittensor): `pip install -e .`, then `python run_local_test.py`, API, and miner template.

### 3. Install PaperForge with Bittensor

```powershell
pip install -e ".[bittensor]"
```

Or install Bittensor separately after the base install:

```powershell
pip install -e .
pip install bittensor
```

---

## Summary of errors and fixes

| Error | Cause | Fix |
|------|--------|-----|
| `bittensor-drand` / "Cargo ... is not installed or is not on PATH" | Rust not installed or not on PATH | Install Rust via rustup.rs; restart terminal; retry `pip install bittensor`. |
| "cannot open input file 'kernel32.lib'" (LNK1181) | Linker can't find Windows SDK libs | Run `scripts\install_bittensor_with_sdk.bat` (sets LIB), or use "Developer Command Prompt for VS 2022". |
| "Could not find directory of OpenSSL installation" (bittensor-wallet) | OpenSSL dev libs not installed or not visible | Install OpenSSL Dev: `winget install ShiningLight.OpenSSL.Dev`. Then run `scripts\install_bittensor_with_sdk.bat` again (it sets `OPENSSL_LIB_DIR` to `...\lib\VC\x64\MD` for that installer). |
| "could not find \`unix\` in \`os\`" / "AsRawFd" / "PermissionsExt" when building bittensor-wallet | bittensor-wallet has no native Windows support | Use **WSL 2** (Ubuntu) to run Bittensor miner/validator and `btcli`. See "Windows: Bittensor and WSL2" below. |
| `numpy` metadata build fails / "Unknown compiler" | Python 3.14 or no C compiler; numpy building from source | Use Python 3.10 or 3.11, or install a C compiler (e.g. Visual Studio Build Tools on Windows). |
| `pip install -e .` works but `paperforge-miner` / `paperforge-validator` fail at runtime | Bittensor not installed | Install with `pip install -e ".[bittensor]"` or `pip install bittensor` (after fixing Rust if needed). |
