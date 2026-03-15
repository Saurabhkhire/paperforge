@echo off
REM ============================================================
REM Install Bittensor (run this from "Developer Command Prompt
REM for VS 2022" or "x64 Native Tools Command Prompt for VS 2022")
REM ============================================================
REM If you get "kernel32.lib not found":
REM   1. Open "Visual Studio Installer"
REM   2. Modify "Build Tools 2022" -> check "Desktop development with C++"
REM   3. Install, then open Developer Command Prompt again and re-run.
REM ============================================================

set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
echo PATH includes cargo. Checking...
where cargo >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: cargo not found. Install Rust from https://rustup.rs/ and restart this prompt.
    exit /b 1
)
cargo --version
echo.
echo Installing Bittensor (this may take several minutes)...
pip install bittensor
set EXIT_CODE=%ERRORLEVEL%
if %EXIT_CODE% NEQ 0 (
    echo.
    echo Install failed. If you see "kernel32.lib" or "LNK1181":
    echo   Install "Desktop development with C++" in Visual Studio Installer, then run this script again from "Developer Command Prompt for VS 2022".
    exit /b %EXIT_CODE%
)
echo.
echo Bittensor installed successfully. Run: btcli --help
exit /b 0
