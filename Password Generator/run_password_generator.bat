@echo off
where py >nul 2>nul
if %errorlevel% equ 0 (
    py "%~dp0password_generator.py"
) else (
    python "%~dp0password_generator.py"
)

if errorlevel 1 (
    echo.
    echo Python 3 was not found. Install Python from https://www.python.org/downloads/
    echo During setup, select "Add Python to PATH", then run this file again.
    pause
)
