@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo        Command Centre Setup (Windows)
echo ========================================
echo.

:: 1. Ask for user name
set /p USER_NAME="Enter your name (press Enter for 'My'): "
if "!USER_NAME!"=="" (
    set "PREFIX=My"
) else (
    set "PREFIX=!USER_NAME!'s"
)

:: 2. Ask for custom app title
set /p APP_TITLE="What do you want to call this app? (press Enter for 'Command Centre'): "
if "!APP_TITLE!"=="" (
    set "APP_TITLE=Command Centre"
)

set "DISPLAY_NAME=!PREFIX! !APP_TITLE!"
echo APP_DISPLAY_NAME="!DISPLAY_NAME!" > .config.env
echo.
echo [OK] Configured as: !DISPLAY_NAME!
echo.

:: 3. Setup virtual environment
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

:: 4. Install dependencies
echo Installing dependencies...
call .venv\Scripts\activate.bat
pip install --quiet -r requirements.txt

echo.
echo ========================================
echo Setup complete! Starting server...
echo Open your browser to: http://localhost:8000
echo ========================================
echo.

uvicorn app:app --port 8000
