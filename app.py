"""
SurakshaTalk Assistant - multilingual safety companion for factory workers.
TCS iON AI Hackathon prototype (single-file Streamlit app).

Run locally:  streamlit run app.py
"""
import io
import json
import os
import random
import re
import threading
import uuid
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

st.set_page_config(page_title="SurakshaTalk", page_icon="🦺", layout="centered")

# ----------------------------------------------------------------------------
# LANGUAGES
# ----------------------------------------------------------------------------
LANGS = {  # code: native name (shown on worker buttons)
    "kn": "ಕನ್ನಡ",
    "hi": "हिन्दी",
    "te": "తెలుగు",
    "ta": "தமிழ்",
    "bn": "বাংলা",
    "en": "English",
}
LANG_EN = {
    "kn": "Kannada", "hi": "Hindi", "te": "Telugu",
    "ta": "Tamil", "bn": "Bengali", "en": "English",
}
WORKER_LANGS = ["kn", "hi", "te", "ta", "bn"]

# ----------------------------------------------------------------------------
# UI TEXT  (NOTE: have native speakers verify before real-world use)
# ----------------------------------------------------------------------------
UI = {
    "en": dict(
        title="SurakshaTalk", choose_lang="Choose your language",
        learn="Learn Safety", ann="Today's Announcements",
        emergency="Emergency Help", listen="Listen", next="Next",
        back="Back", quiz="Quiz", correct="Correct answer!",
        wrong="Not correct.", right_was="Correct answer:",
        feedback_q="How was this lesson?", clear="Clear",
        confusing="Confusing", not_relevant="Not relevant",
        thanks="Thank you!", home="Home", choose_topic="Choose a topic",
        change_lang="Change language", continue_="Continue",
        ann_q="Did you understand?",
        ai_q="Try an AI question", ai_warn="AI-written question. It may have mistakes.",
    ),
    "kn": dict(
        title="ಸುರಕ್ಷಾ ಟಾಕ್", choose_lang="ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        learn="ಸುರಕ್ಷತೆ ಕಲಿಯಿರಿ", ann="ಇಂದಿನ ಪ್ರಕಟಣೆಗಳು",
        emergency="ತುರ್ತು ಸಹಾಯ", listen="ಕೇಳಿ", next="ಮುಂದೆ",
        back="ಹಿಂದೆ", quiz="ರಸಪ್ರಶ್ನೆ", correct="ಸರಿಯಾದ ಉತ್ತರ!",
        wrong="ಸರಿಯಲ್ಲ.", right_was="ಸರಿಯಾದ ಉತ್ತರ:",
        feedback_q="ಈ ಪಾಠ ಹೇಗಿತ್ತು?", clear="ಸ್ಪಷ್ಟ",
        confusing="ಗೊಂದಲ", not_relevant="ಸಂಬಂಧವಿಲ್ಲ",
        thanks="ಧನ್ಯವಾದಗಳು!", home="ಮುಖಪುಟ", choose_topic="ವಿಷಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        change_lang="ಭಾಷೆ ಬದಲಿಸಿ", continue_="ಮುಂದುವರಿಸಿ",
        ann_q="ನಿಮಗೆ ಅರ್ಥವಾಯಿತೇ?",
        ai_q="AI ಪ್ರಶ್ನೆ ಪ್ರಯತ್ನಿಸಿ", ai_warn="AI ಬರೆದ ಪ್ರಶ್ನೆ. ತಪ್ಪುಗಳಿರಬಹುದು.",
    ),
    "hi": dict(
        title="सुरक्षा टॉक", choose_lang="अपनी भाषा चुनें",
        learn="सुरक्षा सीखें", ann="आज की सूचनाएँ",
        emergency="आपातकालीन सहायता", listen="सुनें", next="आगे",
        back="पीछे", quiz="प्रश्नोत्तरी", correct="सही जवाब!",
        wrong="सही नहीं।", right_was="सही जवाब:",
        feedback_q="यह पाठ कैसा था?", clear="साफ़",
        confusing="उलझन भरा", not_relevant="काम का नहीं",
        thanks="धन्यवाद!", home="मुख्य पृष्ठ", choose_topic="विषय चुनें",
        change_lang="भाषा बदलें", continue_="जारी रखें",
        ann_q="क्या आप समझ गए?",
        ai_q="AI प्रश्न आज़माएँ", ai_warn="AI द्वारा लिखा प्रश्न। इसमें गलतियाँ हो सकती हैं।",
    ),
    "te": dict(
        title="సురక్షా టాక్", choose_lang="మీ భాషను ఎంచుకోండి",
        learn="భద్రత నేర్చుకోండి", ann="నేటి ప్రకటనలు",
        emergency="అత్యవసర సహాయం", listen="వినండి", next="తదుపరి",
        back="వెనుకకు", quiz="క్విజ్", correct="సరైన సమాధానం!",
        wrong="సరికాదు.", right_was="సరైన సమాధానం:",
        feedback_q="ఈ పాఠం ఎలా ఉంది?", clear="స్పష్టం",
        confusing="గందరగోళం", not_relevant="సంబంధం లేదు",
        thanks="ధన్యవాదాలు!", home="హోమ్", choose_topic="అంశాన్ని ఎంచుకోండి",
        change_lang="భాష మార్చండి", continue_="కొనసాగించండి",
        ann_q="మీకు అర్థమైందా?",
        ai_q="AI ప్రశ్న ప్రయత్నించండి", ai_warn="AI రాసిన ప్రశ్న. తప్పులు ఉండవచ్చు.",
    ),
    "ta": dict(
        title="சுரக்ஷா டாக்", choose_lang="உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்",
        learn="பாதுகாப்பைக் கற்றுக்கொள்ளுங்கள்", ann="இன்றைய அறிவிப்புகள்",
        emergency="அவசர உதவி", listen="கேளுங்கள்", next="அடுத்து",
        back="பின்", quiz="வினாடி வினா", correct="சரியான பதில்!",
        wrong="சரியல்ல.", right_was="சரியான பதில்:",
        feedback_q="இந்தப் பாடம் எப்படி இருந்தது?", clear="தெளிவு",
        confusing="குழப்பம்", not_relevant="தொடர்பில்லை",
        thanks="நன்றி!", home="முகப்பு", choose_topic="தலைப்பைத் தேர்ந்தெடுக்கவும்",
        change_lang="மொழியை மாற்றவும்", continue_="தொடரவும்",
        ann_q="உங்களுக்குப் புரிந்ததா?",
        ai_q="AI கேள்வியை முயற்சிக்கவும்", ai_warn="AI எழுதிய கேள்வி. தவறுகள் இருக்கலாம்.",
    ),
    "bn": dict(
        title="সুরক্ষা টক", choose_lang="আপনার ভাষা বেছে নিন",
        learn="নিরাপত্তা শিখুন", ann="আজকের ঘোষণা",
        emergency="জরুরি সাহায্য", listen="শুনুন", next="পরবর্তী",
        back="পিছনে", quiz="কুইজ", correct="সঠিক উত্তর!",
        wrong="ঠিক নয়।", right_was="সঠিক উত্তর:",
        feedback_q="এই পাঠটি কেমন ছিল?", clear="স্পষ্ট",
        confusing="বিভ্রান্তিকর", not_relevant="প্রাসঙ্গিক নয়",
        thanks="ধন্যবাদ!", home="হোম", choose_topic="বিষয় বেছে নিন",
        change_lang="ভাষা পরিবর্তন করুন", continue_="চালিয়ে যান",
        ann_q="আপনি কি বুঝেছেন?",
        ai_q="AI প্রশ্ন চেষ্টা করুন", ai_warn="AI-লিখিত প্রশ্ন। ভুল থাকতে পারে।",
    ),
}

# ----------------------------------------------------------------------------
# SAFETY CONTENT  (demo content - factory-specific rules differ by site)
# ----------------------------------------------------------------------------
TOPICS = {
    "ppe": {
        "icon": "🪖",
        "icons": ["🪖", "🥾", "🥽"],
        "name": {
            "en": "Protective Gear (PPE)",
            "kn": "ವೈಯಕ್ತಿಕ ರಕ್ಷಣಾ ಸಾಧನ (PPE)",
            "hi": "सुरक्षा उपकरण (PPE)",
            "te": "రక్షణ పరికరాలు (PPE)",
            "ta": "பாதுகாப்பு உபகரணங்கள் (PPE)",
            "bn": "সুরক্ষা সরঞ্জাম (PPE)",
        },
        "steps": {
            "en": [
                "Wear your helmet before you enter the factory floor.",
                "Wear safety shoes and gloves for your work.",
                "Wear safety glasses when a machine makes dust or sparks.",
            ],
            "kn": [
                "ಕಾರ್ಖಾನೆಯ ಒಳಗೆ ಹೋಗುವ ಮೊದಲು ಹೆಲ್ಮೆಟ್ ಧರಿಸಿ.",
                "ಕೆಲಸಕ್ಕಾಗಿ ಸುರಕ್ಷತಾ ಶೂ ಮತ್ತು ಕೈಗವಸು ಧರಿಸಿ.",
                "ಯಂತ್ರದಿಂದ ಧೂಳು ಅಥವಾ ಕಿಡಿ ಬಂದರೆ ಸುರಕ್ಷತಾ ಕನ್ನಡಕ ಧರಿಸಿ.",
            ],
            "hi": [
                "फैक्ट्री के अंदर जाने से पहले हेलमेट पहनें।",
                "काम के लिए सुरक्षा जूते और दस्ताने पहनें।",
                "जब मशीन से धूल या चिंगारी निकले, तो सुरक्षा चश्मा पहनें।",
            ],
            "te": [
                "ఫ్యాక్టరీ లోపలికి వెళ్లే ముందు హెల్మెట్ ధరించండి.",
                "పని కోసం భద్రతా బూట్లు మరియు చేతి గ్లవుజులు ధరించండి.",
                "యంత్రం నుండి ధూళి లేదా నిప్పురవ్వలు వస్తే భద్రతా కళ్లజోడు ధరించండి.",
            ],
            "ta": [
                "தொழிற்சாலைக்குள் செல்வதற்கு முன் ஹெல்மெட் அணியுங்கள்.",
                "வேலைக்கு பாதுகாப்பு காலணிகளும் கையுறைகளும் அணியுங்கள்.",
                "இயந்திரத்தில் இருந்து தூசி அல்லது தீப்பொறி வந்தால் பாதுகாப்புக் கண்ணாடி அணியுங்கள்.",
            ],
            "bn": [
                "কারখানার ভিতরে যাওয়ার আগে হেলমেট পরুন।",
                "কাজের জন্য নিরাপত্তা জুতো ও দস্তানা পরুন।",
                "মেশিন থেকে ধুলো বা ফুলকি বের হলে নিরাপত্তা চশমা পরুন।",
            ],
        },
        "q": {
            "en": "A machine is throwing sparks. What should you wear?",
            "kn": "ಯಂತ್ರದಿಂದ ಕಿಡಿಗಳು ಹಾರುತ್ತಿವೆ. ನೀವು ಏನು ಧರಿಸಬೇಕು?",
            "hi": "मशीन से चिंगारियाँ निकल रही हैं। आपको क्या पहनना चाहिए?",
            "te": "యంత్రం నుండి నిప్పురవ్వలు వస్తున్నాయి. మీరు ఏమి ధరించాలి?",
            "ta": "இயந்திரத்தில் இருந்து தீப்பொறிகள் பறக்கின்றன. நீங்கள் என்ன அணிய வேண்டும்?",
            "bn": "মেশিন থেকে ফুলকি বের হচ্ছে। আপনার কী পরা উচিত?",
        },
        # first option is always the correct one; display order is shuffled
        "opts": {
            "en": ["Safety glasses", "Slippers", "Nothing"],
            "kn": ["ಸುರಕ್ಷತಾ ಕನ್ನಡಕ", "ಚಪ್ಪಲಿ", "ಏನೂ ಬೇಡ"],
            "hi": ["सुरक्षा चश्मा", "चप्पल", "कुछ नहीं"],
            "te": ["భద్రతా కళ్లజోడు", "చెప్పులు", "ఏమీ వద్దు"],
            "ta": ["பாதுகாப்புக் கண்ணாடி", "செருப்பு", "எதுவும் வேண்டாம்"],
            "bn": ["নিরাপত্তা চশমা", "চপ্পল", "কিছু না"],
        },
    },
    "machine": {
        "icon": "⚙️",
        "icons": ["⛔", "🔌", "🛑"],
        "name": {
            "en": "Machine Safety",
            "kn": "ಯಂತ್ರ ಸುರಕ್ಷತೆ",
            "hi": "मशीन सुरक्षा",
            "te": "యంత్ర భద్రత",
            "ta": "இயந்திரப் பாதுகாப்பு",
            "bn": "মেশিন নিরাপত্তা",
        },
        "steps": {
            "en": [
                "Never touch a machine that is running.",
                "Switch off the machine before cleaning it.",
                "If something looks wrong, press the red stop button and tell your supervisor.",
            ],
            "kn": [
                "ಚಾಲನೆಯಲ್ಲಿರುವ ಯಂತ್ರವನ್ನು ಎಂದಿಗೂ ಮುಟ್ಟಬೇಡಿ.",
                "ಯಂತ್ರವನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸುವ ಮೊದಲು ಅದನ್ನು ಆಫ್ ಮಾಡಿ.",
                "ಏನಾದರೂ ತಪ್ಪಾಗಿ ಕಂಡರೆ ಕೆಂಪು ಸ್ಟಾಪ್ ಬಟನ್ ಒತ್ತಿ ಮತ್ತು ನಿಮ್ಮ ಮೇಲ್ವಿಚಾರಕರಿಗೆ ತಿಳಿಸಿ.",
            ],
            "hi": [
                "चलती हुई मशीन को कभी न छुएँ।",
                "सफाई से पहले मशीन बंद करें।",
                "कुछ गड़बड़ दिखे तो लाल स्टॉप बटन दबाएँ और अपने सुपरवाइज़र को बताएँ।",
            ],
            "te": [
                "నడుస్తున్న యంత్రాన్ని ఎప్పుడూ ముట్టుకోకండి.",
                "శుభ్రం చేసే ముందు యంత్రాన్ని ఆఫ్ చేయండి.",
                "ఏదైనా తప్పుగా అనిపిస్తే ఎరుపు స్టాప్ బటన్ నొక్కి, మీ సూపర్‌వైజర్‌కు చెప్పండి.",
            ],
            "ta": [
                "இயங்கிக் கொண்டிருக்கும் இயந்திரத்தை ஒருபோதும் தொடாதீர்கள்.",
                "சுத்தம் செய்வதற்கு முன் இயந்திரத்தை அணைக்கவும்.",
                "ஏதாவது தவறாகத் தெரிந்தால் சிவப்பு நிறுத்த பொத்தானை அழுத்தி உங்கள் மேற்பார்வையாளரிடம் சொல்லுங்கள்.",
            ],
            "bn": [
                "চলন্ত মেশিন কখনও ছোঁবেন না।",
                "পরিষ্কার করার আগে মেশিন বন্ধ করুন।",
                "কিছু ঠিক না লাগলে লাল স্টপ বোতাম টিপুন এবং আপনার সুপারভাইজারকে জানান।",
            ],
        },
        "q": {
            "en": "You see smoke coming from a machine. What do you do first?",
            "kn": "ಯಂತ್ರದಿಂದ ಹೊಗೆ ಬರುತ್ತಿದೆ. ನೀವು ಮೊದಲು ಏನು ಮಾಡಬೇಕು?",
            "hi": "मशीन से धुआँ निकल रहा है। आप सबसे पहले क्या करेंगे?",
            "te": "యంత్రం నుండి పొగ వస్తోంది. మీరు ముందుగా ఏమి చేయాలి?",
            "ta": "இயந்திரத்தில் இருந்து புகை வருகிறது. நீங்கள் முதலில் என்ன செய்ய வேண்டும்?",
            "bn": "মেশিন থেকে ধোঁয়া বের হচ্ছে। আপনি প্রথমে কী করবেন?",
        },
        "opts": {
            "en": ["Press the red stop button", "Keep working", "Touch the machine"],
            "kn": ["ಕೆಂಪು ಸ್ಟಾಪ್ ಬಟನ್ ಒತ್ತಿ", "ಕೆಲಸ ಮುಂದುವರಿಸಿ", "ಯಂತ್ರವನ್ನು ಮುಟ್ಟಿ"],
            "hi": ["लाल स्टॉप बटन दबाएँ", "काम जारी रखें", "मशीन को छुएँ"],
            "te": ["ఎరుపు స్టాప్ బటన్ నొక్కండి", "పని కొనసాగించండి", "యంత్రాన్ని ముట్టుకోండి"],
            "ta": ["சிவப்பு நிறுத்த பொத்தானை அழுத்துங்கள்", "வேலையைத் தொடருங்கள்", "இயந்திரத்தைத் தொடுங்கள்"],
            "bn": ["লাল স্টপ বোতাম টিপুন", "কাজ চালিয়ে যান", "মেশিন ছুঁয়ে দেখুন"],
        },
    },
}

EMERGENCY = {
    "icons": ["🛑", "🚪", "📞"],
    "steps": {
        "en": ["Press the red stop button.", "Walk to the green exit sign. Do not run.", "Tell your supervisor."],
        "kn": ["ಕೆಂಪು ಸ್ಟಾಪ್ ಬಟನ್ ಒತ್ತಿ.", "ಹಸಿರು ನಿರ್ಗಮನ ಚಿಹ್ನೆಯ ಕಡೆಗೆ ನಡೆಯಿರಿ. ಓಡಬೇಡಿ.", "ನಿಮ್ಮ ಮೇಲ್ವಿಚಾರಕರಿಗೆ ತಿಳಿಸಿ."],
        "hi": ["लाल स्टॉप बटन दबाएँ।", "हरे निकास चिह्न की ओर चलें। दौड़ें नहीं।", "अपने सुपरवाइज़र को बताएँ।"],
        "te": ["ఎరుపు స్టాప్ బటన్ నొక్కండి.", "ఆకుపచ్చ నిష్క్రమణ గుర్తు వైపు నడవండి. పరుగెత్తకండి.", "మీ సూపర్‌వైజర్‌కు చెప్పండి."],
        "ta": ["சிவப்பு நிறுத்த பொத்தானை அழுத்துங்கள்.", "பச்சை வெளியேறும் குறியை நோக்கி நடந்து செல்லுங்கள். ஓடாதீர்கள்.", "உங்கள் மேற்பார்வையாளரிடம் சொல்லுங்கள்."],
        "bn": ["লাল স্টপ বোতাম টিপুন।", "সবুজ বেরোনোর চিহ্নের দিকে হেঁটে যান। দৌড়াবেন না।", "আপনার সুপারভাইজারকে জানান।"],
    },
}

SEED_ANNOUNCEMENT = {
    "en": ["Wear your helmet on the factory floor today.", "Safety drill at 3 PM. Listen for the siren."],
    "kn": ["ಇಂದು ಕಾರ್ಖಾನೆಯಲ್ಲಿ ಹೆಲ್ಮೆಟ್ ಧರಿಸಿ.", "ಮಧ್ಯಾಹ್ನ 3 ಗಂಟೆಗೆ ಸುರಕ್ಷತಾ ಅಭ್ಯಾಸ ನಡೆಯುತ್ತದೆ. ಸೈರನ್ ಕೇಳಿ."],
    "hi": ["आज फैक्ट्री में हेलमेट पहनें।", "दोपहर 3 बजे सुरक्षा अभ्यास होगा। सायरन सुनें।"],
    "te": ["ఈ రోజు ఫ్యాక్టరీలో హెల్మెట్ ధరించండి.", "మధ్యాహ్నం 3 గంటలకు భద్రతా డ్రిల్ ఉంటుంది. సైరన్ వినండి."],
    "ta": ["இன்று தொழிற்சாலையில் ஹெல்மெட் அணியுங்கள்.", "மதியம் 3 மணிக்கு பாதுகாப்பு ஒத்திகை நடைபெறும். சைரன் ஒலியைக் கேளுங்கள்."],
    "bn": ["আজ কারখানায় হেলমেট পরুন।", "বিকেল ৩টায় নিরাপত্তা মহড়া হবে। সাইরেন শুনুন।"],
}

# ----------------------------------------------------------------------------
# SHARED IN-MEMORY STORE (anonymous; resets when the app restarts)
# ----------------------------------------------------------------------------
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


def log(event, topic, value):
    store = get_store()
    with store["lock"]:
        store["rows"].append(dict(ts=datetime.now(), sid=st.session_state.sid,
                                  lang=st.session_state.lang, topic=topic,
                                  event=event, value=value, source="live"))


def summarize(text, max_bullets=4):
    """Simple rule-based summarizer: split into sentences, keep the first few."""
    parts = re.split(r"(?<=[.!?।])\s+|\n+", text.strip())
    parts = [p.strip() for p in parts if p.strip()]
    return parts[:max_bullets]


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


# ----------------------------------------------------------------------------
# TEXT-TO-SPEECH (gTTS needs internet; fails gracefully)
# ----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def tts_bytes(text, lang):
    try:
        from gtts import gTTS
        buf = io.BytesIO()
        gTTS(text=text, lang=lang).write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return None


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
    .stApp {
        background:
          radial-gradient(circle at 12% 8%, rgba(27,138,58,.14) 0, transparent 38%),
          radial-gradient(circle at 90% 20%, rgba(255,193,7,.20) 0, transparent 34%),
          radial-gradient(circle at 20% 95%, rgba(33,150,243,.12) 0, transparent 36%),
          linear-gradient(160deg, #eaf6ec 0%, #fffaf0 100%);
    }
    .block-container {
        background: rgba(255,255,255,.88); border-radius: 22px;
        padding: 1.5rem 1.4rem 2rem 1.4rem; margin-top: 1rem;
        box-shadow: 0 8px 30px rgba(0,0,0,.08); max-width: 760px;
    }
    #MainMenu, footer { visibility: hidden; }
    .stButton > button { min-height: 3.6rem; font-size: 1.2rem; border-radius: 14px; }
    .big-icon { font-size: 6rem; text-align: center; line-height: 1.2; }
    .step-text { font-size: 1.7rem; text-align: center; padding: 0.5rem 0 1rem 0; }
    .title { text-align:center; font-size: 2.2rem; font-weight: 700; color:#1b8a3a; }
    .emerg { background:#fdecea; border:3px solid #d93025; border-radius:16px; padding:1rem; }
    .bullet { font-size: 1.5rem; padding: .4rem 0; }
    .hero { background: linear-gradient(135deg,#1b8a3a,#0f5c26); color:#fff; border-radius:18px;
            padding: 1.4rem 1rem; text-align:center; margin-bottom: 1rem; }
    .hero h1 { margin:0; font-size:2.3rem; color:#fff; }
    .hero p { margin:.4rem 0 0 0; font-size:1.05rem; opacity:.95; }
    .feat { background:#f4faf5; border:1px solid #cfe8d4; border-radius:14px;
            padding:.7rem .6rem; text-align:center; height: 100%; }
    .feat .ic { font-size:1.8rem; }
    .feat .nm { font-weight:700; margin-top:.2rem; }
    .feat .ds { font-size:.85rem; color:#444; }
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
FEATURES = [
    ("🌐", "Language selection", "Kannada, Hindi, Telugu, Tamil, Bengali"),
    ("📘", "Safety learning", "Short steps with big icons and audio"),
    ("❓", "Quiz + AI question", "Checks real understanding, not just a nod"),
    ("😊", "Feedback loop", "Clear / Confusing / Not relevant"),
    ("📢", "Daily announcements", "Short bullets in your language"),
    ("📊", "Supervisor dashboard", "Anonymous language-gap analytics"),
]


def page_lang():
    st.markdown(
        "<div class='hero'><h1>🦺 SurakshaTalk</h1>"
        "<p>Safety explained in the language you understand.</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<h3 style='text-align:center'>🌐 Choose your language / ಭಾಷೆ / भाषा</h3>",
                unsafe_allow_html=True)
    cols = st.columns(2)
    for i, code in enumerate(["kn", "hi", "te", "ta", "bn", "en"]):
        with cols[i % 2]:
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
    pin = os.environ.get("SUPERVISOR_PIN")
    if pin:
        return pin
    try:
        return str(st.secrets["SUPERVISOR_PIN"])
    except Exception:
        return "1234"  # demo default


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
        st.bar_chart(pv)

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
