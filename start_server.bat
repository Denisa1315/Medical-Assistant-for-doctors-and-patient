@echo off
TITLE Medical Assistant Server
COLOR 0A

echo Starting Medical Assistant System...
echo ================================

REM Check MySQL Service
net start MySQL80
if %ERRORLEVEL% NEQ 0 (
    echo Failed to start MySQL. Please check MySQL installation.
    pause
    exit /b 1
)

REM Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Start Flask server
python backend.py

pause