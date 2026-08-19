@echo off
where py >nul 2>&1 && (
    py rock_paper_scissors.py
    exit /b
)

where python >nul 2>&1 && (
    python rock_paper_scissors.py
    exit /b
)

echo Python 3 was not found.
echo Install Python from https://www.python.org/downloads/ and run this file again.
pause
