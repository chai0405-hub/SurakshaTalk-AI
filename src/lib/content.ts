// All worker-facing content. Lessons are written in English and Hindi;
// other languages fall back to English text while the UI labels are translated.

export type Lang = "en" | "hi" | "kn" | "te" | "ta" | "bn";

export const LANGS: { code: Lang; name: string; native: string; speech: string }[] = [
  { code: "en", name: "English", native: "English", speech: "en-IN" },
  { code: "hi", name: "Hindi", native: "हिन्दी", speech: "hi-IN" },
  { code: "kn", name: "Kannada", native: "ಕನ್ನಡ", speech: "kn-IN" },
  { code: "te", name: "Telugu", native: "తెలుగు", speech: "te-IN" },
  { code: "ta", name: "Tamil", native: "தமிழ்", speech: "ta-IN" },
  { code: "bn", name: "Bengali", native: "বাংলা", speech: "bn-IN" },
];

type T = Partial<Record<Lang, string>> & { en: string };

export const UI: Record<string, T> = {
  emergency: { en: "Emergency Help", hi: "आपातकालीन मदद", kn: "ತುರ್ತು ಸಹಾಯ", te: "అత్యవసర సహాయం", ta: "அவசர உதவி", bn: "জরুরি সাহায্য" },
  lessons: { en: "Safety Lessons", hi: "सुरक्षा पाठ", kn: "ಸುರಕ್ಷತಾ ಪಾಠಗಳು", te: "భద్రతా పాఠాలు", ta: "பாதுகாப்பு பாடங்கள்", bn: "নিরাপত্তা পাঠ" },
  hr: { en: "HR Rules", hi: "एचआर नियम", kn: "HR ನಿಯಮಗಳು", te: "HR నియమాలు", ta: "HR விதிகள்", bn: "HR নিয়ম" },
  announcements: { en: "Daily Announcements", hi: "आज की सूचनाएँ", kn: "ದೈನಂದಿನ ಪ್ರಕಟಣೆಗಳು", te: "రోజువారీ ప్రకటనలు", ta: "தினசரி அறிவிப்புகள்", bn: "দৈনিক ঘোষণা" },
  feedback: { en: "Give Feedback", hi: "राय दें", kn: "ಪ್ರತಿಕ್ರಿಯೆ ನೀಡಿ", te: "అభిప్రాయం ఇవ్వండి", ta: "கருத்து தெரிவி", bn: "মতামত দিন" },
  speak: { en: "Tap and speak", hi: "दबाएँ और बोलें", kn: "ಒತ್ತಿ ಮಾತನಾಡಿ", te: "నొక్కి మాట్లాడండి", ta: "தட்டி பேசுங்கள்", bn: "চাপুন ও বলুন" },
  listening: { en: "Listening…", hi: "सुन रहा है…", kn: "ಕೇಳುತ್ತಿದೆ…", te: "వింటోంది…", ta: "கேட்கிறது…", bn: "শুনছে…" },
  listen: { en: "Listen", hi: "सुनें", kn: "ಕೇಳಿ", te: "వినండి", ta: "கேள்", bn: "শুনুন" },
  next: { en: "Next", hi: "आगे", kn: "ಮುಂದೆ", te: "తదుపరి", ta: "அடுத்து", bn: "পরবর্তী" },
  back: { en: "Back", hi: "पीछे", kn: "ಹಿಂದೆ", te: "వెనుకకు", ta: "பின்", bn: "পিছনে" },
  startQ: { en: "Start questions", hi: "प्रश्न शुरू करें", kn: "ಪ್ರಶ್ನೆ ಆರಂಭಿಸಿ", te: "ప్రశ్నలు ప్రారంభించండి", ta: "கேள்விகள் தொடங்கு", bn: "প্রশ্ন শুরু করুন" },
  step: { en: "Step", hi: "चरण", kn: "ಹಂತ", te: "దశ", ta: "படி", bn: "ধাপ" },
  correct: { en: "Correct!", hi: "सही!", kn: "ಸರಿ!", te: "సరైనది!", ta: "சரி!", bn: "সঠিক!" },
  wrong: { en: "Not correct.", hi: "सही नहीं।", kn: "ಸರಿಯಲ್ಲ.", te: "సరికాదు.", ta: "தவறு.", bn: "সঠিক নয়।" },
  clearQ: { en: "Was this easy to understand?", hi: "क्या यह समझना आसान था?", kn: "ಇದು ಅರ್ಥವಾಯಿತೇ?", te: "ఇది సులభంగా అర్థమైందా?", ta: "இது புரிந்ததா?", bn: "এটা কি বোঝা সহজ ছিল?" },
  clear: { en: "Clear", hi: "साफ़", kn: "ಸ್ಪಷ್ಟ", te: "స్పష్టం", ta: "தெளிவு", bn: "পরিষ্কার" },
  confusing: { en: "Confusing", hi: "उलझन", kn: "ಗೊಂದಲ", te: "గందరగోళం", ta: "குழப்பம்", bn: "বিভ্রান্তিকর" },
  irrelevant: { en: "Not relevant", hi: "काम का नहीं", kn: "ಸಂಬಂಧವಿಲ್ಲ", te: "సంబంధం లేదు", ta: "தொடர்பில்லை", bn: "প্রাসঙ্গিক নয়" },
  done: { en: "Lesson complete", hi: "पाठ पूरा", kn: "ಪಾಠ ಮುಗಿದಿದೆ", te: "పాఠం పూర్తైంది", ta: "பாடம் முடிந்தது", bn: "পাঠ শেষ" },
  home: { en: "Home", hi: "होम", kn: "ಮುಖಪುಟ", te: "హోమ్", ta: "முகப்பு", bn: "হোম" },
  fire: { en: "If there is FIRE", hi: "अगर आग लगे", kn: "ಬೆಂಕಿ ಆದರೆ", te: "అగ్ని ఉంటే", ta: "தீ பிடித்தால்", bn: "আগুন লাগলে" },
  injured: { en: "If someone is INJURED", hi: "अगर कोई घायल हो", kn: "ಯಾರಾದರೂ ಗಾಯಗೊಂಡರೆ", te: "ఎవరైనా గాయపడితే", ta: "யாராவது காயமடைந்தால்", bn: "কেউ আহত হলে" },
  call: { en: "Call Safety Desk · 112", hi: "सुरक्षा डेस्क को कॉल · 112", kn: "ಸುರಕ್ಷತಾ ಡೆಸ್ಕ್ ಕರೆ · 112", te: "సేఫ్టీ డెస్క్ కాల్ · 112", ta: "பாதுகாப்பு மேசை அழை · 112", bn: "সেফটি ডেস্কে কল · 112" },
  check: { en: "Check your understanding", hi: "अपनी समझ जाँचें", kn: "ತಿಳುವಳಿಕೆ ಪರಿಶೀಲಿಸಿ", te: "మీ అవగాహన చూడండి", ta: "புரிதலை சரிபார்", bn: "বোঝা যাচাই করুন" },
  noAnn: { en: "No announcements yet today.", hi: "आज कोई सूचना नहीं।", kn: "ಇಂದು ಪ್ರಕಟಣೆ ಇಲ್ಲ.", te: "ఈరోజు ప్రకటనలు లేవు.", ta: "இன்று அறிவிப்பு இல்லை.", bn: "আজ কোনো ঘোষণা নেই।" },
  comment: { en: "Say or type a comment (optional)", hi: "टिप्पणी बोलें या लिखें (वैकल्पिक)", kn: "ಅಭಿಪ್ರಾಯ ಹೇಳಿ/ಬರೆಯಿರಿ", te: "వ్యాఖ్య చెప్పండి/రాయండి", ta: "கருத்து சொல்லுங்கள்/எழுதுங்கள்", bn: "মন্তব্য বলুন বা লিখুন" },
  send: { en: "Send anonymously", hi: "गुमनाम भेजें", kn: "ಅನಾಮಧೇಯವಾಗಿ ಕಳುಹಿಸಿ", te: "అనామకంగా పంపండి", ta: "அநாமதேயமாக அனுப்பு", bn: "বেনামে পাঠান" },
  thanks: { en: "Thank you! Your feedback is anonymous.", hi: "धन्यवाद! आपकी राय गुमनाम है।", kn: "ಧನ್ಯವಾದ! ನಿಮ್ಮ ಅಭಿಪ್ರಾಯ ಅನಾಮಧೇಯ.", te: "ధన్యవాదాలు! మీ అభిప్రాయం అనామకం.", ta: "நன்றி! உங்கள் கருத்து அநாமதேயம்.", bn: "ধন্যবাদ! আপনার মতামত বেনামী।" },
  supervisor: { en: "Supervisor", hi: "सुपरवाइज़र", kn: "ಮೇಲ್ವಿಚಾರಕ", te: "సూపర్‌వైజర్", ta: "மேற்பார்வையாளர்", bn: "সুপারভাইজার" },
};

export const tr = (key: string, lang: Lang) => UI[key]?.[lang] ?? UI[key]?.en ?? key;
export const pick = (t: T, lang: Lang) => t[lang] ?? t.en;

export type IconName =
  | "power" | "lock" | "hand" | "hardhat" | "glasses" | "ear" | "flame" | "door" | "extinguisher"
  | "calendar" | "wallet" | "shield" | "clock" | "cog";

export type Topic = {
  id: string;
  group: "safety" | "hr";
  icon: IconName;
  title: T;
  steps: { icon: IconName; text: T }[];
  quiz: { q: T; options: T[]; answer: number; explain: T }[];
};

export const TOPICS: Topic[] = [
  {
    id: "machines", group: "safety", icon: "cog",
    title: { en: "Working with Machines", hi: "मशीन के साथ काम" },
    steps: [
      { icon: "power", text: { en: "Before cleaning or fixing, switch the machine OFF.", hi: "साफ़ करने या ठीक करने से पहले मशीन बंद करें।" } },
      { icon: "lock", text: { en: "Put your own lock and tag on the switch.", hi: "स्विच पर अपना ताला और टैग लगाएँ।" } },
      { icon: "hand", text: { en: "Never put your hand inside a running machine.", hi: "चलती मशीन में कभी हाथ न डालें।" } },
    ],
    quiz: [
      { q: { en: "The belt is stuck. What do you do first?", hi: "बेल्ट अटक गई है। पहले क्या करेंगे?" },
        options: [{ en: "Pull it with your hand", hi: "हाथ से खींचें" }, { en: "Switch OFF and lock", hi: "बंद करें और ताला लगाएँ" }, { en: "Hit it with a tool", hi: "औज़ार से मारें" }],
        answer: 1, explain: { en: "Always switch OFF and lock before touching.", hi: "छूने से पहले हमेशा बंद करें और ताला लगाएँ।" } },
      { q: { en: "Who can remove your lock?", hi: "आपका ताला कौन हटा सकता है?" },
        options: [{ en: "Anyone on the shift", hi: "शिफ्ट का कोई भी" }, { en: "The next worker", hi: "अगला कर्मचारी" }, { en: "Only you", hi: "सिर्फ़ आप" }],
        answer: 2, explain: { en: "Only you remove your own lock. This keeps you safe.", hi: "सिर्फ़ आप अपना ताला हटाते हैं। इससे आप सुरक्षित रहते हैं।" } },
    ],
  },
  {
    id: "ppe", group: "safety", icon: "hardhat",
    title: { en: "Using Helmet & Gloves", hi: "हेलमेट और दस्ताने" },
    steps: [
      { icon: "hardhat", text: { en: "Wear your helmet before entering the line.", hi: "लाइन में जाने से पहले हेलमेट पहनें।" } },
      { icon: "hand", text: { en: "Wear gloves. Change torn gloves at once.", hi: "दस्ताने पहनें। फटे दस्ताने तुरंत बदलें।" } },
      { icon: "glasses", text: { en: "Wear eye and ear protection where signs show it.", hi: "जहाँ निशान हो, आँख और कान की सुरक्षा पहनें।" } },
    ],
    quiz: [
      { q: { en: "Your glove tears while the machine is running. What do you do first?", hi: "मशीन चलते समय दस्ताना फट गया। पहले क्या करेंगे?" },
        options: [{ en: "Stop the machine", hi: "मशीन रोकें" }, { en: "Keep working carefully", hi: "सावधानी से काम करते रहें" }, { en: "Remove both gloves", hi: "दोनों दस्ताने उतारें" }],
        answer: 0, explain: { en: "First, always stop the machine. Then change the glove.", hi: "पहले मशीन रोकें। फिर दस्ताना बदलें।" } },
      { q: { en: "A friend enters without a helmet. What should you do?", hi: "दोस्त बिना हेलमेट आया। आप क्या करेंगे?" },
        options: [{ en: "Ignore it", hi: "अनदेखा करें" }, { en: "Remind them, tell supervisor if needed", hi: "याद दिलाएँ, ज़रूरत हो तो सुपरवाइज़र को बताएँ" }, { en: "Give them your helmet", hi: "अपना हेलमेट दें" }],
        answer: 1, explain: { en: "Remind them kindly. Safety is everyone's job.", hi: "प्यार से याद दिलाएँ। सुरक्षा सबका काम है।" } },
    ],
  },
  {
    id: "fire", group: "safety", icon: "flame",
    title: { en: "Fire and Smoke", hi: "आग और धुआँ" },
    steps: [
      { icon: "flame", text: { en: "See fire or smoke? Shout 'FIRE' and press the alarm.", hi: "आग या धुआँ दिखे? 'आग' चिल्लाएँ और अलार्म दबाएँ।" } },
      { icon: "extinguisher", text: { en: "Small fire: use the red extinguisher only if trained.", hi: "छोटी आग: प्रशिक्षित हों तभी लाल अग्निशामक इस्तेमाल करें।" } },
      { icon: "door", text: { en: "Big fire: do not fight. Walk to the green EXIT and assembly point.", hi: "बड़ी आग: न लड़ें। हरे EXIT और इकट्ठा स्थान पर जाएँ।" } },
    ],
    quiz: [
      { q: { en: "There is a lot of smoke. Can you use the lift?", hi: "बहुत धुआँ है। क्या लिफ्ट ले सकते हैं?" },
        options: [{ en: "Yes, it is faster", hi: "हाँ, जल्दी है" }, { en: "No, use the stairs", hi: "नहीं, सीढ़ियाँ लें" }],
        answer: 1, explain: { en: "Never use the lift in a fire. Use stairs.", hi: "आग में कभी लिफ्ट न लें। सीढ़ियाँ लें।" } },
    ],
  },
  {
    id: "leave", group: "hr", icon: "calendar",
    title: { en: "Attendance & Leave", hi: "हाज़िरी और छुट्टी" },
    steps: [
      { icon: "clock", text: { en: "Punch your card at the start and end of every shift.", hi: "हर शिफ्ट की शुरुआत और अंत में कार्ड पंच करें।" } },
      { icon: "calendar", text: { en: "Ask for planned leave at least 2 days before.", hi: "तय छुट्टी कम से कम 2 दिन पहले माँगें।" } },
      { icon: "shield", text: { en: "Sick? Call your supervisor before the shift starts.", hi: "बीमार हैं? शिफ्ट से पहले सुपरवाइज़र को फ़ोन करें।" } },
    ],
    quiz: [
      { q: { en: "You have a wedding next week. When do you ask for leave?", hi: "अगले हफ़्ते शादी है। छुट्टी कब माँगेंगे?" },
        options: [{ en: "On the same day", hi: "उसी दिन" }, { en: "At least 2 days before", hi: "कम से कम 2 दिन पहले" }, { en: "After coming back", hi: "लौटने के बाद" }],
        answer: 1, explain: { en: "Ask at least 2 days before so the shift can be planned.", hi: "2 दिन पहले माँगें ताकि शिफ्ट तय हो सके।" } },
    ],
  },
  {
    id: "pay", group: "hr", icon: "wallet",
    title: { en: "Salary & Overtime", hi: "वेतन और ओवरटाइम" },
    steps: [
      { icon: "wallet", text: { en: "Salary comes to your bank on the 7th of every month.", hi: "वेतन हर महीने की 7 तारीख़ को बैंक में आता है।" } },
      { icon: "clock", text: { en: "Overtime is paid at double rate.", hi: "ओवरटाइम दोगुनी दर से मिलता है।" } },
      { icon: "shield", text: { en: "Check your payslip. Ask HR if anything is wrong.", hi: "पे-स्लिप जाँचें। गलत हो तो HR से पूछें।" } },
    ],
    quiz: [
      { q: { en: "How is overtime paid?", hi: "ओवरटाइम कैसे मिलता है?" },
        options: [{ en: "Not paid", hi: "नहीं मिलता" }, { en: "Normal rate", hi: "सामान्य दर" }, { en: "Double rate", hi: "दोगुनी दर" }],
        answer: 2, explain: { en: "Overtime is always paid at double rate.", hi: "ओवरटाइम हमेशा दोगुनी दर से मिलता है।" } },
    ],
  },
  {
    id: "harassment", group: "hr", icon: "lock",
    title: { en: "Reporting Harassment", hi: "उत्पीड़न की शिकायत" },
    steps: [
      { icon: "shield", text: { en: "Nobody may shout at, touch or threaten you.", hi: "कोई आप पर चिल्ला, छू या धमका नहीं सकता।" } },
      { icon: "ear", text: { en: "Tell HR or drop a note in the complaint box.", hi: "HR को बताएँ या शिकायत बॉक्स में पर्ची डालें।" } },
      { icon: "lock", text: { en: "Your complaint is private. You cannot lose your job for reporting.", hi: "आपकी शिकायत गोपनीय है। शिकायत करने से नौकरी नहीं जाएगी।" } },
    ],
    quiz: [
      { q: { en: "Can you lose your job for reporting harassment?", hi: "क्या शिकायत करने से नौकरी जा सकती है?" },
        options: [{ en: "Yes", hi: "हाँ" }, { en: "No", hi: "नहीं" }],
        answer: 1, explain: { en: "Reporting is protected. Your job is safe.", hi: "शिकायत सुरक्षित है। आपकी नौकरी सुरक्षित है।" } },
    ],
  },
];

export const EMERGENCY = {
  fire: [
    { icon: "flame", text: { en: "Shout FIRE and press the red alarm.", hi: "आग चिल्लाएँ और लाल अलार्म दबाएँ।" } },
    { icon: "door", text: { en: "Walk to the nearest green EXIT. Do not use the lift.", hi: "नज़दीकी हरे EXIT पर जाएँ। लिफ्ट न लें।" } },
    { icon: "shield", text: { en: "Go to the assembly point and wait for a head count.", hi: "इकट्ठा स्थान पर जाएँ और गिनती का इंतज़ार करें।" } },
  ],
  injured: [
    { icon: "power", text: { en: "Stop the machine. Do not move the injured person.", hi: "मशीन रोकें। घायल को न हिलाएँ।" } },
    { icon: "phone", text: { en: "Call the safety desk or first-aider now.", hi: "अभी सुरक्षा डेस्क या प्राथमिक उपचारकर्ता को बुलाएँ।" } },
    { icon: "plus", text: { en: "Stay with them. Press a clean cloth on bleeding.", hi: "उनके साथ रहें। खून पर साफ़ कपड़ा दबाएँ।" } },
  ],
} as const;
