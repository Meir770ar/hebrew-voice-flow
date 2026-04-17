@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ===================================================
echo  Hebrew Voice Flow - Setup
echo ===================================================
echo.

REM --- Python check ---
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Install Python 3.11+ from https://python.org
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] Python !PYVER! detected

REM --- Pick mode ---
echo.
echo Which version do you want to install?
echo   [1] Local only - Whisper transcription, no AI, no internet needed
echo   [2] With AI   - adds Groq rewording (requires free API key)
echo.
set /p MODE="Choose 1 or 2: "

if "%MODE%"=="1" (
    set REQFILE=requirements.txt
    echo [setup] installing LOCAL-ONLY dependencies...
) else if "%MODE%"=="2" (
    set REQFILE=requirements-ai.txt
    echo [setup] installing AI-MODE dependencies...
) else (
    echo [ERROR] Invalid choice
    pause
    exit /b 1
)

REM --- Install ---
python -m pip install --upgrade pip >nul
python -m pip install -r %REQFILE%
if errorlevel 1 (
    echo [ERROR] pip install failed
    pause
    exit /b 1
)

REM --- Mode-specific config ---
if "%MODE%"=="2" (
    echo.
    echo  How to get a free Groq API key:
    echo    1. Go to https://console.groq.com/keys
    echo    2. Sign in with Google / GitHub / email
    echo    3. Click "Create API Key"
    echo    4. Copy the key ^(starts with gsk_...^)
    echo.
    echo  No credit card required. 14,400 free requests/day.
    echo  Full guide: docs\groq-api-key.md
    echo.
    set /p GROQKEY="Paste your key here (or press Enter to skip): "
    if "!GROQKEY!"=="" (
        echo [WARN] no key entered - AI will be disabled until you set GROQ_API_KEY
    ) else (
        echo GROQ_API_KEY=!GROQKEY!> .env
        echo [OK] API key saved to .env (gitignored)
    )
)

echo.
echo ===================================================
echo  Setup complete
echo ===================================================
echo.
echo To run:
echo   run.bat            - silent background
echo   run-debug.bat      - with console logs
echo.
echo Hotkeys:
if "%MODE%"=="2" (
    echo   Right Ctrl  = raw transcription
    echo   Right Alt   = AI cleanup ^(punctuation, fillers^)
    echo   Right Shift = AI dev-request ^(rewrite for Claude Code^)
) else (
    echo   Right Ctrl  = raw transcription
)
echo.
pause
