@echo off
REM Set LIB so link.exe can find kernel32.lib (Windows SDK), then install Bittensor.
REM Use this if you get LNK1181: cannot open input file 'kernel32.lib'
REM bittensor-wallet also needs OpenSSL: set OPENSSL_DIR to your OpenSSL install (see INSTALL.md).

set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"
set "WIN_KITS=C:\Program Files (x86)\Windows Kits\10"
set "MSVC_BASE=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC"
set "MSVC_VER=14.44.35207"

REM Windows SDK libs (x64) - kernel32.lib lives here
set "LIB=%WIN_KITS%\Lib\10.0.18362.0\um\x64;%WIN_KITS%\Lib\10.0.18362.0\ucrt\x64"
REM MSVC libs (x64)
set "LIB=%LIB%;%MSVC_BASE%\%MSVC_VER%\lib\x64"
if not exist "%WIN_KITS%\Lib\10.0.18362.0\um\x64\kernel32.lib" (
    if exist "%WIN_KITS%\Lib\10.0.22621.0\um\x64\kernel32.lib" set "LIB=%WIN_KITS%\Lib\10.0.22621.0\um\x64;%WIN_KITS%\Lib\10.0.22621.0\ucrt\x64;%MSVC_BASE%\%MSVC_VER%\lib\x64"
    if exist "%WIN_KITS%\Lib\10.0.19041.0\um\x64\kernel32.lib" set "LIB=%WIN_KITS%\Lib\10.0.19041.0\um\x64;%WIN_KITS%\Lib\10.0.19041.0\ucrt\x64;%MSVC_BASE%\%MSVC_VER%\lib\x64"
)

echo LIB set for Windows SDK + MSVC.

REM bittensor-wallet needs OpenSSL (lib + include). ShiningLight OpenSSL uses lib\VC\x64\MD for .lib files.
if not defined OPENSSL_DIR (
    if exist "C:\Program Files\OpenSSL-Win64\include\openssl\ssl.h" (
        set "OPENSSL_DIR=C:\Program Files\OpenSSL-Win64"
        if exist "C:\Program Files\OpenSSL-Win64\lib\VC\x64\MD\libcrypto.lib" set "OPENSSL_LIB_DIR=C:\Program Files\OpenSSL-Win64\lib\VC\x64\MD"
        if exist "C:\Program Files\OpenSSL-Win64\lib\VC\x64\MD\libcrypto.lib" set "OPENSSL_INCLUDE_DIR=C:\Program Files\OpenSSL-Win64\include"
    )
    if exist "C:\Program Files (x86)\OpenSSL-Win64\include\openssl\ssl.h" (
        set "OPENSSL_DIR=C:\Program Files (x86)\OpenSSL-Win64"
        if exist "C:\Program Files (x86)\OpenSSL-Win64\lib\VC\x64\MD\libcrypto.lib" set "OPENSSL_LIB_DIR=C:\Program Files (x86)\OpenSSL-Win64\lib\VC\x64\MD"
        if exist "C:\Program Files (x86)\OpenSSL-Win64\lib\VC\x64\MD\libcrypto.lib" set "OPENSSL_INCLUDE_DIR=C:\Program Files (x86)\OpenSSL-Win64\include"
    )
)
if defined OPENSSL_DIR (
    if not defined OPENSSL_LIB_DIR if exist "%OPENSSL_DIR%\lib\VC\x64\MD\libcrypto.lib" set "OPENSSL_LIB_DIR=%OPENSSL_DIR%\lib\VC\x64\MD"
    if not defined OPENSSL_INCLUDE_DIR if exist "%OPENSSL_DIR%\include\openssl\ssl.h" set "OPENSSL_INCLUDE_DIR=%OPENSSL_DIR%\include"
)
if defined OPENSSL_DIR echo OPENSSL_DIR=%OPENSSL_DIR%
if defined OPENSSL_LIB_DIR echo OPENSSL_LIB_DIR=%OPENSSL_LIB_DIR%
if defined OPENSSL_INCLUDE_DIR echo OPENSSL_INCLUDE_DIR=%OPENSSL_INCLUDE_DIR%
if not defined OPENSSL_DIR (
    echo.
    echo bittensor-wallet requires OpenSSL. Install "OpenSSL Dev" via: winget install ShiningLight.OpenSSL.Dev
    echo Then run this script again.
    echo.
)

echo Installing Bittensor...
pip install bittensor
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo If kernel32.lib: run from "Developer Command Prompt for VS 2022".
    echo If OpenSSL: install ShiningLight.OpenSSL.Dev and re-run.
    echo If "could not find unix in os" or "AsRawFd": bittensor-wallet has no Windows support. Use WSL2 (see INSTALL.md).
    exit /b 1
)
echo Bittensor installed. Run: btcli --help
exit /b 0
