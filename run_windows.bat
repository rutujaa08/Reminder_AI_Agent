@echo off
title RemindMe AI - Reminder System
cd /d "%~dp0"
echo ============================================
echo         RemindMe AI - Starting app
echo ============================================
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.9 or newer from python.org
  echo During installation, select "Add Python to PATH".
  pause
  exit /b 1
)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo Installation failed. Check your internet connection and Python setup.
  pause
  exit /b 1
)
python -m streamlit run app.py
pause
