"""
SurakshaTalk Assistant - multilingual safety companion for factory workers.
TCS iON AI Hackathon prototype (Streamlit app: screens in app.py, data in utils/).

Run locally:  streamlit run app.py
"""
import random
import uuid

import pandas as pd
import streamlit as st

from utils.content import (EMERGENCY, FEATURES, LANG_EN, LANGS, TOPICS, UI)
from utils.services import ai_enabled, generate_ai_question, get_secret, tts_bytes
from utils.store import get_store, log_event, summarize

st.set_page_config(page_title="SurakshaTalk", page_icon="🦺", layout="centered")

# ----------------------------------------------------------------------------
# LANGUAGES
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# UI TEXT  (NOTE: have native speakers verify before real-world use)
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# SAFETY CONTENT  (demo content - factory-specific rules differ by site)
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# SHARED IN-MEMORY STORE (anonymous; resets when the app restarts)
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# TEXT-TO-SPEECH (gTTS needs internet; fails gracefully)
# ----------------------------------------------------------------------------


def speak(text, key):
    if st.button("🔊 " + t("listen"), key=key, width="stretch"):
        audio = tts_bytes(text, st.session_state.lang)
        if audio:
            st.audio(audio, format="audio/mp3")
        else:
            st.warning("Audio unavailable right now (internet needed).")


# ----------------------------------------------------------------------------
# STATE + NAVIGATION HELPERS
# ----------------------------------------------------------------------------
ss = st.session_state
if "sid" not in ss:
    ss.sid = uuid.uuid4().hex[:8]
    ss.page = "lang"
    ss.lang = "en"
    ss.topic = None
    ss.step = 0
    ss.quiz_result = None
    ss.ann_logged = False
    ss.sup_ok = False
    ss.ai_q = None
    ss.ai_result = None
    ss.ai_request = False
    ss.ai_err = False


def t(key):
    return UI[ss.lang][key]


def go(page):
    ss.page = page


def pick_lang(code):
    ss.lang = code
    ss.page = "home"


def open_topic(tid):
    ss.topic = tid
    ss.step = 0
    ss.quiz_result = None
    ss.ai_q = None
    ss.ai_result = None
    ss.ai_request = False
    ss.ai_err = False
    ss.page = "lesson"


def set_step(n):
    ss.step = n


def log(event, topic, value):
    log_event(ss.sid, ss.lang, topic, event, value)


def submit_quiz(orig_idx):
    ok = orig_idx == 0
    ss.quiz_result = {"picked": orig_idx, "ok": ok}
    log("quiz", ss.topic, "correct" if ok else "incorrect")


def request_ai():
    ss.ai_request = True
    ss.ai_err = False


def submit_ai(orig_idx):
    ok = orig_idx == 0
    ss.ai_result = {"ok": ok}
    log("ai_quiz", ss.topic, "correct" if ok else "incorrect")


def submit_feedback(value):
    log("feedback", ss.topic, value)
    ss.step = 5


def submit_ann(value):
    log("announcement", "announcements", value)
    ss.ann_logged = True


def logout():
    ss.sup_ok = False
    ss.page = "lang"


# ----------------------------------------------------------------------------
# STYLE
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Theme-neutral design: works in BOTH light and dark mode.
       We never paint a solid card behind text; we only add soft glows on top of
       whatever background the device uses, and style our own buttons explicitly. */
    .stApp {
        background-image:
          radial-gradient(circle at 8% 4%,  rgba(27,138,58,.30) 0, transparent 42%),
          radial-gradient(circle at 96% 12%, rgba(255,193,7,.22) 0, transparent 36%),
          radial-gradient(circle at 10% 98%, rgba(33,150,243,.20) 0, transparent 42%),
          radial-gradient(circle at 92% 92%, rgba(27,138,58,.24) 0, transparent 40%);
        background-repeat: no-repeat;
    }
    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }
    .block-container { max-width: 760px; padding-top: 2.5rem; padding-bottom: 3rem; }

    /* Buttons: always green with white text, in every state */
    .stButton button, .stFormSubmitButton button {
        min-height: 3.6rem; font-size: 1.2rem; border-radius: 14px;
        background: linear-gradient(135deg, #1b8a3a, #146c2d) !important;
        color: #ffffff !important; border: none !important;
        box-shadow: 0 3px 10px rgba(0,0,0,.22);
    }
    .stButton button p, .stFormSubmitButton button p { color: #ffffff !important; font-size: 1.3rem; }
    .stButton button:hover, .stButton button:focus, .stButton button:focus-visible,
    .stFormSubmitButton button:hover, .stFormSubmitButton button:focus {
        background: linear-gradient(135deg, #23a548, #1b8a3a) !important;
        color: #ffffff !important; border: none !important; box-shadow: 0 4px 14px rgba(0,0,0,.28);
    }
    .stButton button:active, .stFormSubmitButton button:active {
        background: #0f5c26 !important; color: #ffffff !important; transform: scale(.985);
    }

    .big-icon { font-size: 6rem; text-align: center; line-height: 1.2; }
    .step-text { font-size: 1.7rem; text-align: center; padding: 0.5rem 0 1rem 0; }
    .title { text-align:center; font-size: 2.2rem; font-weight: 700; color:#1fa74a; }
    .bullet { font-size: 1.5rem; padding: .4rem 0; }
    .emerg { background: rgba(217,48,37,.16); border: 3px solid #d93025;
             border-radius: 16px; padding: 1rem; }
    .hero { background: linear-gradient(135deg,#1b8a3a,#0f5c26); border-radius: 18px;
            padding: 1.4rem 1rem; text-align: center; margin-bottom: 1rem;
            box-shadow: 0 6px 18px rgba(0,0,0,.25); }
    .hero h1, .hero p { color: #ffffff !important; }
    .hero h1 { margin: 0; font-size: 2.3rem; }
    .hero p { margin: .4rem 0 0 0; font-size: 1.05rem; opacity: .95; }
    .feat { background: rgba(27,138,58,.14); border: 1px solid rgba(27,138,58,.40);
            border-radius: 14px; padding: .7rem .6rem; text-align: center; height: 100%; }
    .feat .ic { font-size: 1.8rem; }
    .feat .nm { font-weight: 700; margin-top: .2rem; }
    .feat .ds { font-size: .85rem; opacity: .8; }
    </style>
    """,
    unsafe_allow_html=True,
)


def header():
    st.markdown(f"<div class='title'>🦺 {t('title')}</div>", unsafe_allow_html=True)


def home_btn():
    st.button("🏠 " + t("home"), on_click=go, args=("home",), width="stretch")


# ----------------------------------------------------------------------------
# WORKER PAGES
# ----------------------------------------------------------------------------


def page_lang():
    st.markdown(
        "<div class='hero'><h1>🦺 SurakshaTalk</h1>"
        "<p>Safety explained in the language you understand.</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<h3 style='text-align:center'>🌐 Choose your language / ಭಾಷೆ / भाषा</h3>",
                unsafe_allow_html=True)
    for code in ["kn", "hi", "te", "ta", "bn", "en"]:
        st.button(LANGS[code], key=f"lang_{code}", on_click=pick_lang,
                  args=(code,), width="stretch")
    st.divider()
    st.markdown("#### ✨ Features")
    for row in range(0, len(FEATURES), 3):
        fc = st.columns(3)
        for col, (ic, nm, ds) in zip(fc, FEATURES[row:row + 3]):
            col.markdown(
                f"<div class='feat'><div class='ic'>{ic}</div>"
                f"<div class='nm'>{nm}</div><div class='ds'>{ds}</div></div>",
                unsafe_allow_html=True)
    st.divider()
    st.button("👷 I am a Supervisor", on_click=go, args=("sup",), width="stretch")


def page_home():
    header()
    st.markdown(f"<h4 style='text-align:center'>{LANGS[ss.lang]}</h4>", unsafe_allow_html=True)
    st.button("📘 " + t("learn"), on_click=go, args=("topics",), width="stretch")
    st.button("📢 " + t("ann"), on_click=lambda: (go("ann"), setattr(ss, "ann_logged", False)),
              width="stretch")
    st.button("🚨 " + t("emergency"), on_click=go, args=("emergency",), width="stretch")
    st.divider()
    st.button("🌐 " + t("change_lang"), on_click=go, args=("lang",), width="stretch")


def page_topics():
    header()
    st.subheader(t("choose_topic"))
    for tid, tp in TOPICS.items():
        st.button(f"{tp['icon']}  {tp['name'][ss.lang]}", key=f"topic_{tid}",
                  on_click=open_topic, args=(tid,), width="stretch")
    home_btn()


def render_ai_question():
    aq = ss.ai_q
    st.markdown("---")
    st.markdown("**🤖 AI**")
    st.markdown(f"<div class='step-text'>{aq['q']}</div>", unsafe_allow_html=True)
    speak(aq["q"], key="speak_ai_q")
    st.caption(t("ai_warn"))
    if ss.ai_result is None:
        order = random.Random(ss.sid + aq["q"]).sample(range(3), 3)
        for orig in order:
            st.button(aq["opts"][orig], key=f"ai_opt_{orig}", on_click=submit_ai,
                      args=(orig,), width="stretch")
    else:
        if ss.ai_result["ok"]:
            st.success("✅ " + t("correct"))
        else:
            st.error("❌ " + t("wrong"))
            st.info(f"{t('right_was')} **{aq['opts'][0]}**")
        st.button(t("continue_") + " ➡️", on_click=set_step, args=(4,), width="stretch")


def page_lesson():
    tp = TOPICS[ss.topic]
    L = ss.lang
    step = ss.step
    header()
    st.caption(tp["name"][L])

    if step < 3:  # --- lesson steps ---
        st.progress((step + 1) / 3)
        st.markdown(f"<div class='big-icon'>{tp['icons'][step]}</div>", unsafe_allow_html=True)
        text = tp["steps"][L][step]
        st.markdown(f"<div class='step-text'>{text}</div>", unsafe_allow_html=True)
        speak(text, key=f"speak_{ss.topic}_{step}")
        c1, c2 = st.columns(2)
        with c1:
            if step > 0:
                st.button("⬅️ " + t("back"), on_click=set_step, args=(step - 1,),
                          width="stretch")
            else:
                st.button("⬅️ " + t("back"), on_click=go, args=("topics",),
                          width="stretch")
        with c2:
            st.button(t("next") + " ➡️", on_click=set_step, args=(step + 1,),
                      width="stretch")

    elif step == 3:  # --- quiz ---
        st.subheader("❓ " + t("quiz"))
        question = tp["q"][L]
        st.markdown(f"<div class='step-text'>{question}</div>", unsafe_allow_html=True)
        speak(question, key=f"speak_q_{ss.topic}")
        opts = tp["opts"][L]
        order = random.Random(ss.sid + ss.topic).sample(range(3), 3)
        if ss.quiz_result is None:
            for orig in order:
                st.button(opts[orig], key=f"opt_{orig}", on_click=submit_quiz,
                          args=(orig,), width="stretch")
        else:
            if ss.ai_request:
                with st.spinner("🤖 ..."):
                    try:
                        ss.ai_q = generate_ai_question(ss.topic, L)
                        ss.ai_result = None
                        ss.ai_err = False
                    except Exception:
                        ss.ai_q = None
                        ss.ai_err = True
                ss.ai_request = False
                st.rerun()
            if ss.ai_q is not None:
                render_ai_question()
            else:
                if ss.quiz_result["ok"]:
                    st.success("✅ " + t("correct"))
                else:
                    st.error("❌ " + t("wrong"))
                    st.info(f"{t('right_was')} **{opts[0]}**")
                if ss.ai_err:
                    st.warning("🤖 AI question unavailable right now.")
                st.button(t("continue_") + " ➡️", on_click=set_step, args=(4,),
                          width="stretch")
                if ai_enabled():
                    st.button("🤖 " + t("ai_q"), on_click=request_ai, width="stretch")

    elif step == 4:  # --- feedback ---
        st.markdown(f"<div class='step-text'>{t('feedback_q')}</div>", unsafe_allow_html=True)
        st.button("😊 " + t("clear"), on_click=submit_feedback, args=("clear",),
                  width="stretch")
        st.button("😕 " + t("confusing"), on_click=submit_feedback, args=("confusing",),
                  width="stretch")
        st.button("🚫 " + t("not_relevant"), on_click=submit_feedback, args=("not_relevant",),
                  width="stretch")

    else:  # --- done ---
        st.markdown("<div class='big-icon'>🎉</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='step-text'>{t('thanks')}</div>", unsafe_allow_html=True)
        st.button("📘 " + t("learn"), on_click=go, args=("topics",), width="stretch")
        home_btn()


def page_ann():
    header()
    st.subheader("📢 " + t("ann"))
    store = get_store()
    with store["lock"]:
        latest = store["announcements"][0] if store["announcements"] else {}
    bullets = latest.get(ss.lang) or latest.get("en") or []
    if not bullets:
        st.info("—")
    for b in bullets:
        st.markdown(f"<div class='bullet'>• {b}</div>", unsafe_allow_html=True)
    if bullets:
        speak(" ".join(bullets), key="speak_ann")
        st.markdown(f"<div class='step-text'>{t('ann_q')}</div>", unsafe_allow_html=True)
        if ss.ann_logged:
            st.success("✅ " + t("thanks"))
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.button("😊 " + t("clear"), on_click=submit_ann, args=("clear",),
                          width="stretch")
            with c2:
                st.button("😕 " + t("confusing"), on_click=submit_ann, args=("confusing",),
                          width="stretch")
    home_btn()


def page_emergency():
    header()
    st.markdown(f"<div class='emerg'><h2>🚨 {t('emergency')}</h2></div>", unsafe_allow_html=True)
    L = ss.lang
    for i, text in enumerate(EMERGENCY["steps"][L]):
        st.markdown(f"<div class='step-text'>{EMERGENCY['icons'][i]} {text}</div>",
                    unsafe_allow_html=True)
    speak(" ".join(EMERGENCY["steps"][L]), key="speak_emerg")
    st.caption("Demo content only. Real emergency steps depend on your factory.")
    home_btn()


# ----------------------------------------------------------------------------
# SUPERVISOR PAGES
# ----------------------------------------------------------------------------
def get_pin():
    return get_secret("SUPERVISOR_PIN", "1234")  # demo default


def page_sup():
    st.markdown("<div class='title'>👷 Supervisor</div>", unsafe_allow_html=True)
    if not ss.sup_ok:
        pin = st.text_input("Enter supervisor PIN", type="password")
        if st.button("Login", width="stretch"):
            if pin == get_pin():
                ss.sup_ok = True
                st.rerun()
            else:
                st.error("Wrong PIN")
        st.button("⬅️ Back", on_click=go, args=("lang",), width="stretch")
        return

    tab1, tab2 = st.tabs(["📊 Analytics", "📢 Announcements"])
    with tab1:
        sup_dashboard()
    with tab2:
        sup_announcements()
    st.button("Logout", on_click=logout, width="stretch")


def sup_dashboard():
    store = get_store()
    with store["lock"]:
        rows = list(store["rows"])
    df = pd.DataFrame(rows)
    st.button("🔄 Refresh", key="refresh_dash", width="stretch")
    include_demo = st.toggle("Include DEMO sample data", value=True)
    if not include_demo:
        df = df[df.source == "live"]
    if df.empty:
        st.info("No live data yet. Complete a lesson as a worker, then come back.")
        return

    df["language"] = df["lang"].map(LANG_EN)
    df["topic_name"] = df["topic"].map(
        lambda x: TOPICS[x]["name"]["en"] if x in TOPICS else "Announcements")
    quiz = df[df.event.isin(["quiz", "ai_quiz"])].copy()
    fb = df[df.event.isin(["feedback", "announcement"])]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sessions", df.sid.nunique())
    c2.metric("Quiz attempts", len(quiz))
    c3.metric("Quiz accuracy", f"{(quiz.value == 'correct').mean() * 100:.0f}%" if len(quiz) else "-")
    c4.metric("'Confusing'", f"{(fb.value == 'confusing').mean() * 100:.0f}%" if len(fb) else "-")
    n_ai = int((df.event == "ai_quiz").sum())
    if n_ai:
        st.caption(f"Includes {n_ai} AI-generated question attempts.")
    if include_demo:
        st.caption("Includes labelled demo sample data - not real worker results.")

    if len(quiz):
        st.markdown("**Quiz accuracy (%) by language and topic**")
        quiz["acc"] = (quiz.value == "correct") * 100
        pv = quiz.pivot_table(index="language", columns="topic_name",
                              values="acc", aggfunc="mean")
        st.bar_chart(pv, stack=False)

        st.markdown("**Weakest spots (lowest accuracy first)**")
        weak = (quiz.groupby(["language", "topic_name"])
                .agg(attempts=("acc", "size"), accuracy_pct=("acc", "mean"))
                .round(0).sort_values("accuracy_pct").reset_index())
        st.dataframe(weak, width="stretch", hide_index=True)

    if len(fb):
        st.markdown("**Clarity feedback**")
        counts = fb.groupby(["topic_name", "value"]).size().unstack(fill_value=0)
        st.bar_chart(counts)

    st.markdown("**Sessions per language**")
    st.bar_chart(df.groupby("language").sid.nunique())


def sup_announcements():
    st.write("Type the announcement in each language (leave blank to skip). "
             "It is summarised into 2-4 short bullets for workers.")
    with st.form("ann_form"):
        inputs = {code: st.text_area(LANG_EN[code], key=f"ann_in_{code}", height=80)
                  for code in ["en", "kn", "hi", "te", "ta", "bn"]}
        submitted = st.form_submit_button("Publish")
    if submitted:
        new = {code: summarize(txt) for code, txt in inputs.items() if txt.strip()}
        if not new:
            st.error("Enter at least one language.")
        else:
            store = get_store()
            with store["lock"]:
                store["announcements"].insert(0, new)
            st.success("Published! Workers will see it under Today's Announcements.")
            for code, bl in new.items():
                st.write(f"**{LANG_EN[code]}**: " + " | ".join(bl))
    st.caption("Tip: translations should be reviewed by a fluent speaker before real use.")


# ----------------------------------------------------------------------------
# ROUTER
# ----------------------------------------------------------------------------
PAGES = {
    "lang": page_lang, "home": page_home, "topics": page_topics,
    "lesson": page_lesson, "ann": page_ann, "emergency": page_emergency,
    "sup": page_sup,
}
PAGES.get(ss.page, page_lang)()
