@echo off
REM Quick Start Script for Credit Default Prediction App (Windows)

echo ================================
echo Credit Default Prediction App
echo Quick Start Setup
echo ================================

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Run the app
echo.
echo ================================
echo Starting Streamlit App...
echo ================================
echo.
echo The app will open at: http://localhost:8501
echo Press Ctrl+C to stop the app
echo.

streamlit run app.py

pause
