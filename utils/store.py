"""Anonymous in-memory store shared across sessions (resets when the app restarts)."""
import random
import re
import threading
from datetime import datetime, timedelta

import streamlit as st

from utils.content import SEED_ANNOUNCEMENT, TOPICS, WORKER_LANGS


def _seed_rows():
    """Clearly-labelled DEMO data so the supervisor dashboard is not empty."""
    rnd = random.Random(7)
    acc = {"te|machine": 0.45, "ta|ppe": 0.55, "bn|machine": 0.6}
    rows = []
    now = datetime.now()
    n = 0
    for lang in WORKER_LANGS:
        for topic in TOPICS:
            p = acc.get(f"{lang}|{topic}", 0.82)
            for _ in range(10):
                n += 1
                sid = f"demo{n}"
                ts = now - timedelta(days=rnd.randint(0, 6), minutes=rnd.randint(0, 600))
                ok = rnd.random() < p
                rows.append(dict(ts=ts, sid=sid, lang=lang, topic=topic, event="quiz",
                                 value="correct" if ok else "incorrect", source="demo"))
                r = rnd.random()
                fb = "clear" if r < p - 0.1 else ("confusing" if r < 0.95 else "not_relevant")
                rows.append(dict(ts=ts, sid=sid, lang=lang, topic=topic, event="feedback",
                                 value=fb, source="demo"))
    return rows


@st.cache_resource
def get_store():
    return {"lock": threading.Lock(), "rows": _seed_rows(),
            "announcements": [dict(SEED_ANNOUNCEMENT)]}


def summarize(text, max_bullets=4):
    """Simple rule-based summarizer: split into sentences, keep the first few."""
    parts = re.split(r"(?<=[.!?।])\s+|\n+", text.strip())
    parts = [p.strip() for p in parts if p.strip()]
    return parts[:max_bullets]


def log_event(sid, lang, topic, event, value):
    """Append one anonymous row (random session id, language, topic, event, value)."""
    store = get_store()
    with store["lock"]:
        store["rows"].append(dict(ts=datetime.now(), sid=sid, lang=lang, topic=topic,
                                  event=event, value=value, source="live"))
