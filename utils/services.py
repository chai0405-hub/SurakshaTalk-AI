"""External helpers: secrets, text-to-speech (gTTS) and optional AI question (Gemini)."""
import io
import json
import os
import re

import streamlit as st

from utils.content import LANG_EN, TOPICS


def get_secret(name, default=None):
    v = os.environ.get(name)
    if v:
        return v
    try:
        return str(st.secrets[name])
    except Exception:
        return default


def ai_enabled():
    return bool(get_secret("GEMINI_API_KEY"))


def generate_ai_question(topic_id, lang):
    """Ask a free-tier Gemini model for ONE new quiz question based only on the lesson.
    Returns {'q': str, 'opts': [correct, wrong, wrong]}. Raises on any failure."""
    import requests
    key = get_secret("GEMINI_API_KEY")
    model = get_secret("GEMINI_MODEL", "gemini-2.0-flash")
    lesson = " ".join(TOPICS[topic_id]["steps"]["en"])
    prompt = (
        "You write very simple factory-safety quiz questions for workers with low literacy. "
        f"Lesson: {lesson}\n"
        f"Write ONE new multiple-choice question in {LANG_EN[lang]} (use that language's own script), "
        "using very simple words, based ONLY on the lesson above. Give exactly 3 short options; "
        "the FIRST option must be the correct one. "
        'Return only JSON: {"question": "...", "options": ["...", "...", "..."]}'
    )
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    r = requests.post(
        url, params={"key": key}, timeout=25,
        json={"contents": [{"parts": [{"text": prompt}]}],
              "generationConfig": {"responseMimeType": "application/json", "temperature": 0.7}},
    )
    r.raise_for_status()
    text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    data = json.loads(text)
    q = str(data["question"]).strip()
    opts = [str(o).strip() for o in data["options"]][:3]
    if not q or len(opts) != 3:
        raise ValueError("bad AI response")
    return {"q": q, "opts": opts}


@st.cache_data(show_spinner=False)
def tts_bytes(text, lang):
    try:
        from gtts import gTTS
        buf = io.BytesIO()
        gTTS(text=text, lang=lang).write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return None
