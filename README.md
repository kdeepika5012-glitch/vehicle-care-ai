# VehicleCare AI
Gemini-powered car and bike maintenance/troubleshooting chatbot.

## Local
pip install -r requirements.txt
Create `.env` with `GEMINI_API_KEY=YOUR_API_KEY`
Run `python app.py`

## Render
Build: `pip install -r requirements.txt`
Start: `gunicorn app:app`
Environment Variable: `GEMINI_API_KEY`
Model: `gemini-3.5-flash`
