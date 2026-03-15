@echo off
REM Run this from "Developer Command Prompt for VS 2022" (or after calling vcvars64.bat)
REM so that link.exe and kernel32.lib (Windows SDK) are available.
REM Then: pip install bittensor

set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
pip install bittensor
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo If you see "kernel32.lib" not found, install the Windows SDK:
    echo - Open Visual Studio Installer, modify Build Tools 2022, add "Windows 10/11 SDK" or "Desktop development with C++"
    echo Then open "Developer Command Prompt for VS 2022" and run this script again.
    exit /b 1
)
echo.
echo Bittensor installed. You can now run scripts\setup_wallets.bat to create miner and validator wallets.
exit /b 0
