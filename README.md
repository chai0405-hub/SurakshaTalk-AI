# SurakshaTalk Assistant

Multilingual safety companion for factory workers (Kannada, Hindi, Telugu, Tamil, Bengali + English).
TCS iON AI Hackathon prototype built with Streamlit.

## Features
- **Language selection**: large touch-friendly buttons
- **Safety learning**: Protective Gear and Machine Safety, with icons, short text and audio (gTTS)
- **Quiz + optional AI question**: scenario quiz with instant feedback; an extra AI-generated question appears if a free Gemini key is set
- **Feedback loop**: Clear / Confusing / Not relevant
- **Daily announcements**: supervisor publishes, rule-based summary into 2-4 bullets
- **Emergency help** screen
- **Supervisor dashboard**: anonymous accuracy by language/topic, weakest spots, feedback counts, sessions per language

## Files
| File | Purpose |
|---|---|
| `app.py` | The whole app |
| `requirements.txt` | Python packages |
| `.streamlit/config.toml` | Theme |
| `.streamlit/secrets.toml.example` | Template for secrets (PIN, optional AI key) |
| `.gitignore` | Keeps secrets and cache out of GitHub |

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Push to GitHub
```bash
cd SurakshaTalk
git init
git add .
git commit -m "SurakshaTalk Assistant"
git branch -M main
git remote add origin https://github.com/<your-username>/surakshatalk.git
git push -u origin main
```
(Create the empty repo on github.com first. No git installed? Use "Add file > Upload files" on GitHub and drag in the folder contents, including the `.streamlit` folder.)

## Deploy on Streamlit Community Cloud
1. Go to https://share.streamlit.io and sign in with GitHub.
2. **Create app** > pick your repo, branch `main`, main file `app.py`.
3. Open **Advanced settings > Secrets** and paste:
   ```
   SUPERVISOR_PIN = "your-pin"
   GEMINI_API_KEY = "your-free-key"   # optional, enables the AI question
   ```
4. Click **Deploy**.

## Supervisor login
Default demo PIN is `1234` unless `SUPERVISOR_PIN` is set.

## Important notes
- **Audio** uses gTTS and needs internet. If it fails, a message is shown and everything else still works.
- **AI questions** are optional, generated live by a model, and can be wrong. The app tells workers so. Do not rely on them for real safety training without review.
- **Data is stored in memory** and resets when the app restarts. It is anonymous (random session ID, language, topic, answer correctness, feedback). No names or biometrics.
- The dashboard includes **labelled DEMO sample data** (toggle it off to see only live data). Do not present it as real results.
- **Translations are AI-written and unverified.** Have a fluent speaker check each language, especially safety wording.
- Safety and emergency content is generic demo content; real procedures depend on the factory.
