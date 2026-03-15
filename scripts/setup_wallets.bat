@echo off
REM Create miner and validator wallets (requires Bittensor/btcli installed).
REM Run: scripts\setup_wallets.bat

set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
btcli --help >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo btcli not found. Install Bittensor first: run scripts\install_bittensor_dev_prompt.bat from Developer Command Prompt.
    exit /b 1
)

echo Creating MINER wallet: miner_cold / default
echo You will be prompted for a password for the coldkey; choose a strong one and back it up.
btcli wallet new_coldkey --wallet.name miner_cold
btcli wallet new_hotkey --wallet.name miner_cold --wallet.hotkey default

echo.
echo Creating VALIDATOR wallet: val_cold / default
btcli wallet new_coldkey --wallet.name val_cold
btcli wallet new_hotkey --wallet.name val_cold --wallet.hotkey default

echo.
echo Done. Back up coldkeys in %USERPROFILE%\.bittensor\wallets\
btcli wallet list
exit /b 0
