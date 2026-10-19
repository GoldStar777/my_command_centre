@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo      Uninstalling Command Centre
echo ========================================
echo.

:: 1. Terminate any active process listening on port 8000
echo Checking for active server on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Terminating server process PID %%a...
    taskkill /F /PID %%a >nul 2>&1
)

echo Server stopped.
echo.

:: 2. Prompt user about data retention
echo How would you like to handle your data?
echo   [1] Keep my database (Tasks, notes, and tags will reload if you reinstall) [Default]
echo   [2] Nuclear Wipe (Permanently delete database, config, virtual environment, and logs)
set /p UNINSTALL_CHOICE="Select an option (1 or 2, default is 1): "

if "%UNINSTALL_CHOICE%"=="2" (
    echo.
    set /p CONFIRM_DELETE="Are you sure? This CANNOT be undone! Type 'DELETE' to confirm: "
    if "!CONFIRM_DELETE!"=="DELETE" (
        echo Performing complete purge...
        if exist ".venv" rmdir /s /q ".venv"
        if exist ".config.env" del /f /q ".config.env"
        del /f /q *.db *.sqlite3 *.log 2>nul
        for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
        echo All user data, virtual environments, and configuration files have been purged.
    ) else (
        echo Confirmation mismatch. Data preserved safely.
    )
) else (
    echo Database and notes kept safe.
)

echo.
echo ========================================
echo Uninstallation complete.
echo ========================================
pause
