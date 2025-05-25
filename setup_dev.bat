@echo off
echo.
echo =====================================
echo  TypoFix Development Setup
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/4] Installing development tools...
pip install black flake8 mypy pytest

echo.
echo =====================================
echo  Setup Complete! 
echo =====================================
echo.
echo To get started:
echo   1. Activate environment: .venv\Scripts\activate
echo   2. Run the app: python app.py
echo   3. Build executable: python build_exe.py
echo.
echo For more information, see README.md and CONTRIBUTING.md
echo.
pause 