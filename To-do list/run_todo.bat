@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
    py todo_app.py
    exit /b %errorlevel%
)

where python >nul 2>nul
if not errorlevel 1 (
    python todo_app.py
    exit /b %errorlevel%
)

echo Python 3 is required to run TaskFlow.
echo Install it from https://www.python.org/downloads/ and select "Add Python to PATH".
pause
exit /b 1
