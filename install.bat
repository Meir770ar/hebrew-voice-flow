@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title Hebrew Voice Flow - One-Click Installer

echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║         Hebrew Voice Flow - Installer            ║
echo  ║         הכתבה קולית בעברית - מתקין אוטומטי       ║
echo  ╚══════════════════════════════════════════════════╝
echo.

set INSTALL_DIR=%USERPROFILE%\hebrew-voice-flow

REM --- Step 1: Python check ---
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python not installed. Installing via winget...
    winget install -e --id Python.Python.3.11 --accept-source-agreements --accept-package-agreements
    if errorlevel 1 (
        echo.
        echo [ERROR] Could not install Python automatically.
        echo Please install Python 3.11+ manually from https://python.org
        echo Then run this installer again.
        pause
        exit /b 1
    )
    echo [OK] Python installed. Please close this window and run the installer again.
    pause
    exit /b 0
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo     Python !PYVER! detected

REM --- Step 2: Git check ---
echo.
echo [2/5] Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo [!] Git not installed. Installing via winget...
    winget install -e --id Git.Git --accept-source-agreements --accept-package-agreements >nul 2>&1
)
echo     Git available

REM --- Step 3: Clone or update ---
echo.
echo [3/5] Downloading Hebrew Voice Flow...
if exist "%INSTALL_DIR%\.git" (
    echo     Already installed at %INSTALL_DIR%, updating...
    cd /d "%INSTALL_DIR%"
    git pull --quiet
) else (
    if exist "%INSTALL_DIR%" rmdir /s /q "%INSTALL_DIR%" 2>nul
    git clone --quiet https://github.com/Meir770ar/hebrew-voice-flow.git "%INSTALL_DIR%"
    if errorlevel 1 (
        echo [ERROR] Download failed. Check your internet connection.
        pause
        exit /b 1
    )
)
cd /d "%INSTALL_DIR%"
echo     Installed at %INSTALL_DIR%

REM --- Step 4: Ask about AI mode ---
echo.
echo [4/5] Choose version:
echo.
echo     [1] Local only     - Whisper transcription, fully offline, no AI
echo     [2] With AI        - Adds Groq text refinement (free API key needed)
echo.
set /p MODE="Choose 1 or 2 [default 1]: "
if "%MODE%"=="" set MODE=1

if "%MODE%"=="2" (
    set REQFILE=requirements-ai.txt
    echo     Installing AI-mode dependencies...
) else (
    set REQFILE=requirements.txt
    echo     Installing local-only dependencies...
)

python -m pip install --upgrade pip --quiet
python -m pip install -r %REQFILE% --quiet
if errorlevel 1 (
    echo [ERROR] Installation failed.
    pause
    exit /b 1
)

REM --- Step 5: AI key setup ---
if "%MODE%"=="2" (
    if not exist ".env" (
        echo.
        echo Get a free Groq API key at: https://console.groq.com/keys
        set /p GROQKEY="Paste your Groq key (or press Enter to skip): "
        if not "!GROQKEY!"=="" (
            echo GROQ_API_KEY=!GROQKEY!> .env
        )
    )
)

REM --- Create desktop shortcut ---
echo.
echo [5/5] Creating desktop shortcut...
powershell -NoProfile -Command ^
    "$ws = New-Object -ComObject WScript.Shell;" ^
    "$sc = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Hebrew Voice Flow.lnk');" ^
    "$sc.TargetPath = '%INSTALL_DIR%\run.bat';" ^
    "$sc.WorkingDirectory = '%INSTALL_DIR%';" ^
    "$sc.IconLocation = 'imageres.dll,138';" ^
    "$sc.Description = 'Hebrew Voice Flow - Voice dictation';" ^
    "$sc.Save();" >nul

REM --- Optional: Auto-start on Windows boot ---
echo.
set /p AUTORUN="Start automatically when Windows boots? [Y/n]: "
if /i "%AUTORUN%" NEQ "n" (
    powershell -NoProfile -Command ^
        "$ws = New-Object -ComObject WScript.Shell;" ^
        "$sc = $ws.CreateShortcut([Environment]::GetFolderPath('Startup') + '\Hebrew Voice Flow.lnk');" ^
        "$sc.TargetPath = '%INSTALL_DIR%\run.bat';" ^
        "$sc.WorkingDirectory = '%INSTALL_DIR%';" ^
        "$sc.WindowStyle = 7;" ^
        "$sc.Save();" >nul
    echo     Auto-start enabled
)

echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║              Installation complete!              ║
echo  ╚══════════════════════════════════════════════════╝
echo.
echo  Installed to:  %INSTALL_DIR%
echo  Desktop icon:  Hebrew Voice Flow
echo.
echo  How to use:
echo    1. Launch from desktop shortcut
echo    2. Hold Right Ctrl, speak, release -- text appears at cursor
echo.
set /p LAUNCH="Launch now? [Y/n]: "
if /i "%LAUNCH%" NEQ "n" (
    start "" "%INSTALL_DIR%\run.bat"
)
exit /b 0
