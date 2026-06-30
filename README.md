# Medication Routine Assistant

An AI agent for daily medication tracking built with Google ADK and Gemini 2.5 Flash.

## What it does
- Add medications with name, dosage, and schedule times
- View a structured daily check-in (Today's medications / Logged so far / Still remaining)
- Log doses as taken, missed, or skipped
- Summarize adherence over time
- Refuses all medical advice and redirects to a doctor or pharmacist

## How to run
```bash
pip install google-adk
export GOOGLE_API_KEY=your_key_here
adk run medication_assistant
```

## Built with
- Google Agent Development Kit (ADK)
- Gemini 2.5 Flash
- Python
- Kaggle AI Capstone 2026
