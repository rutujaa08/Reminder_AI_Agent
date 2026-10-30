# RemindMe AI — Reminder System (Single AI Agent)

A beginner-friendly Streamlit application for creating, searching, filtering, and completing reminders.

## Features
- Interactive sidebar navigation: Dashboard, Add Reminder, My Reminders, Smart Quick Add, Insights, About
- Add reminders with date, time, category, notes, and priority
- Quick-add helper understands common words such as today, tomorrow, morning, afternoon, evening, and night
- Search/filter reminders, mark complete, reopen, and delete
- Productivity insights and JSON export
- Local persistence through `reminders.json`
- No API key required

## Run on Windows
1. Extract `Reminder_AI_Agent.zip`.
2. Open the `Reminder_AI_Agent` folder.
3. Double-click `run_windows.bat`.
4. If the browser does not open automatically, visit `http://localhost:8501`.

Alternative:
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Requirements
- Python 3.9+
- Internet connection for first-time package installation

## Important
This is a project demo. It does not send push notifications, SMS, or email and cannot alert you while the app is closed. Quick Add uses simple rule-based parsing, not a connected large language model. To build a production reminder service, add a scheduler/background service and a notification provider, with user consent.
