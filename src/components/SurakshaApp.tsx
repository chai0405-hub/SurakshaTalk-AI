import { useEffect, useMemo, useState, type ReactNode } from "react";
import {
  Siren, BookOpen, Briefcase, Megaphone, MessageSquare, Mic, Languages, Home, Volume2, Check, X,
  Power, Lock, Hand, HardHat, Glasses, Ear, Flame, DoorOpen, FireExtinguisher, Calendar, Wallet,
  Shield, Clock, Cog, Phone, Plus, ThumbsUp, Frown, Ban, Star, UserCog, type LucideIcon,
} from "lucide-react";
import { LANGS, TOPICS, EMERGENCY, tr, pick, type Lang, type Topic } from "@/lib/content";
import { store, summarize, type Feedback } from "@/lib/store";

const ICONS = {
  power: Power, lock: Lock, hand: Hand, hardhat: HardHat, glasses: Glasses, ear: Ear, flame: Flame,
  door: DoorOpen, extinguisher: FireExtinguisher, calendar: Calendar, wallet: Wallet, shield: Shield,
  clock: Clock, cog: Cog, phone: Phone, plus: Plus,
} satisfies Record<string, LucideIcon>;

type Screen =
  | { s: "home" } | { s: "lang" } | { s: "emergency" } | { s: "list"; group: "safety" | "hr" }
  | { s: "lesson"; id: string } | { s: "quiz"; id: string } | { s: "done"; id: string }
  | { s: "ann" } | { s: "feedback" } | { s: "sup" };

function speak(text: string, lang: Lang) {
  if (typeof window === "undefined" || !window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = LANGS.find((l) => l.code === lang)?.speech ?? "en-IN";
  u.rate = 0.9;
  window.speechSynthesis.speak(u);
}

function listen(lang: Lang, onText: (t: string) => void, onEnd: () => void) {
  const W = window as unknown as { SpeechRecognition?: new () => any; webkitSpeechRecognition?: new () => any };
  const R = W.SpeechRecognition ?? W.webkitSpeechRecognition;
  if (!R) { alert("Voice input is not supported in this browser. Try Chrome."); onEnd(); return; }
  const r = new R();
  r.lang = LANGS.find((l) => l.code === lang)?.speech ?? "en-IN";
  r.onresult = (e: any) => onText(String(e.results[0][0].transcript).toLowerCase());
  r.onend = onEnd;
  r.onerror = onEnd;
  r.start();
}

export function SurakshaApp() {
  const [screen, go] = useState<Screen>({ s: "home" });
  const [lang, setLangState] = useState<Lang>("en");
  useEffect(() => setLangState(store.lang()), []);
  const setLang = (l: Lang) => { setLangState(l); store.setLang(l); };
  const t = (k: string) => tr(k, lang);

  return (
    <div className="min-h-screen bg-background">
      <div className="hazard-stripe" />
      <main className="mx-auto max-w-md px-4 pb-10 pt-4">
        {screen.s === "home" && <HomeScreen t={t} lang={lang} go={go} />}
        {screen.s === "lang" && <LangScreen lang={lang} setLang={(l) => { setLang(l); speak(LANGS.find((x) => x.code === l)!.native, l); go({ s: "home" }); }} go={go} />}
        {screen.s === "emergency" && <EmergencyScreen t={t} lang={lang} go={go} />}
        {screen.s === "list" && <ListScreen t={t} lang={lang} go={go} group={screen.group} />}
        {screen.s === "lesson" && <LessonScreen t={t} lang={lang} go={go} topic={TOPICS.find((x) => x.id === screen.id)!} />}
        {screen.s === "quiz" && <QuizScreen t={t} lang={lang} go={go} topic={TOPICS.find((x) => x.id === screen.id)!} />}
        {screen.s === "done" && <DoneScreen t={t} lang={lang} go={go} topic={TOPICS.find((x) => x.id === screen.id)!} />}
        {screen.s === "ann" && <AnnScreen t={t} lang={lang} go={go} />}
        {screen.s === "feedback" && <FeedbackScreen t={t} lang={lang} go={go} topicId="general" title={t("feedback")} />}
        {screen.s === "sup" && <SupervisorScreen go={go} />}
      </main>
    </div>
  );
}

type P = { t: (k: string) => string; lang: Lang; go: (s: Screen) => void };

function Header({ title, go, right }: { title: string; go?: (s: Screen) => void; right?: ReactNode }) {
  return (
    <div className="mb-4 flex items-center justify-between gap-3">
      <h1 className="font-display text-xl text-foreground">{title}</h1>
      {right ?? (go && (
        <button aria-label="Home" onClick={() => go({ s: "home" })} className="chunky grid h-11 w-11 place-items-center rounded-full bg-card">
          <Home className="h-5 w-5" />
        </button>
      ))}
    </div>
  );
}

function ListenBtn({ text, label, lang }: { text: string; label: string; lang: Lang }) {
  return (
    <button onClick={() => speak(text, lang)} className="chunky inline-flex items-center gap-1.5 rounded-full bg-primary px-3 py-1.5 text-sm font-semibold text-primary-foreground">
      <Volume2 className="h-4 w-4" /> {label}
    </button>
  );
}

function Tile({ icon: I, label, onClick, tone = "card" }: { icon: LucideIcon; label: string; onClick: () => void; tone?: "card" | "primary" }) {
  return (
    <button onClick={onClick} className={`chunky flex min-h-32 flex-col justify-between rounded-2xl p-4 text-left ${tone === "primary" ? "bg-primary text-primary-foreground" : "bg-card text-card-foreground"}`}>
      <I className="h-8 w-8" strokeWidth={2.2} />
      <span className="text-base font-bold leading-tight">{label}</span>
    </button>
  );
}

function BigBtn({ children, onClick, tone = "primary", className = "" }: { children: ReactNode; onClick: () => void; tone?: "primary" | "dark" | "card" | "danger"; className?: string }) {
  const tones = { primary: "bg-primary text-primary-foreground", dark: "bg-secondary text-secondary-foreground", card: "bg-card text-card-foreground", danger: "bg-destructive text-destructive-foreground" };
  return <button onClick={onClick} className={`chunky flex w-full items-center justify-center gap-2 rounded-2xl px-4 py-4 text-base font-bold ${tones[tone]} ${className}`}>{children}</button>;
}

function HomeScreen({ t, lang, go }: P) {
  const [listening, setListening] = useState(false);
  const voice = () => {
    setListening(true);
    listen(lang, (txt) => {
      if (/fire|emergency|help|आग|मदद|injur|घायल/.test(txt)) go({ s: "emergency" });
      else if (/hr|leave|salary|छुट्टी|वेतन/.test(txt)) go({ s: "list", group: "hr" });
      else if (/announce|news|सूचना/.test(txt)) go({ s: "ann" });
      else if (/feedback|राय/.test(txt)) go({ s: "feedback" });
      else go({ s: "list", group: "safety" });
    }, () => setListening(false));
  };
  return (
    <>
      <Header title="SurakshaTalk" right={
        <button onClick={() => go({ s: "lang" })} className="chunky inline-flex items-center gap-1.5 rounded-full bg-card px-3 py-2 text-sm font-semibold">
          <Languages className="h-4 w-4" /> {LANGS.find((l) => l.code === lang)?.native}
        </button>
      } />
      <BigBtn tone="danger" onClick={() => go({ s: "emergency" })} className="mb-4 justify-start py-6 text-lg">
        <Siren className="h-7 w-7" /> {t("emergency")}
      </BigBtn>
      <div className="grid grid-cols-2 gap-3">
        <Tile icon={BookOpen} tone="primary" label={t("lessons")} onClick={() => go({ s: "list", group: "safety" })} />
        <Tile icon={Briefcase} label={t("hr")} onClick={() => go({ s: "list", group: "hr" })} />
        <Tile icon={Megaphone} label={t("announcements")} onClick={() => go({ s: "ann" })} />
        <Tile icon={MessageSquare} label={t("feedback")} onClick={() => go({ s: "feedback" })} />
      </div>
      <BigBtn tone="dark" onClick={voice} className="mt-4">
        <Mic className="h-5 w-5" /> {listening ? t("listening") : t("speak")}
      </BigBtn>
      <button onClick={() => go({ s: "sup" })} className="mx-auto mt-8 flex items-center gap-1.5 text-sm font-semibold text-muted-foreground underline">
        <UserCog className="h-4 w-4" /> {t("supervisor")}
      </button>
    </>
  );
}

function LangScreen({ lang, setLang, go }: { lang: Lang; setLang: (l: Lang) => void; go: (s: Screen) => void }) {
  return (
    <>
      <Header title="Language · भाषा" go={go} />
      <div className="grid grid-cols-2 gap-3">
        {LANGS.map((l) => (
          <button key={l.code} onClick={() => setLang(l.code)} className={`chunky rounded-2xl p-5 text-left ${l.code === lang ? "bg-primary text-primary-foreground" : "bg-card"}`}>
            <div className="text-2xl font-bold">{l.native}</div>
            <div className="text-sm text-muted-foreground">{l.name}</div>
          </button>
        ))}
      </div>
    </>
  );
}

function EmergencyScreen({ t, lang, go }: P) {
  const [kind, setKind] = useState<"fire" | "injured">("injured");
  const steps = EMERGENCY[kind];
  const all = steps.map((s) => pick(s.text, lang)).join(" ");
  useEffect(() => { speak(all, lang); }, [kind]); // auto-play
  return (
    <>
      <Header title={t("emergency")} go={go} />
      <div className="mb-4 grid grid-cols-2 gap-3">
        <button onClick={() => setKind("fire")} className={`chunky flex flex-col items-center gap-2 rounded-2xl bg-destructive p-4 font-bold text-destructive-foreground ${kind === "fire" ? "ring-4 ring-ring" : ""}`}>
          <Flame className="h-8 w-8" /> {t("fire")}
        </button>
        <button onClick={() => setKind("injured")} className={`chunky flex flex-col items-center gap-2 rounded-2xl bg-accent p-4 font-bold text-accent-foreground ${kind === "injured" ? "ring-4 ring-ring" : ""}`}>
          <Plus className="h-8 w-8" /> {t("injured")}
        </button>
      </div>
      <ol className="space-y-3">
        {steps.map((s, i) => {
          const I = ICONS[s.icon];
          return (
            <li key={i} className="chunky flex items-center gap-3 rounded-2xl bg-card p-4">
              <span className="font-display text-xl">{i + 1}</span>
              <I className="h-7 w-7 shrink-0" />
              <span className="font-semibold">{pick(s.text, lang)}</span>
            </li>
          );
        })}
      </ol>
      <div className="mt-4"><ListenBtn text={all} label={t("listen")} lang={lang} /></div>
      <a href="tel:112" className="chunky mt-5 flex w-full items-center justify-center gap-2 rounded-2xl bg-secondary py-4 font-bold text-secondary-foreground">
        <Phone className="h-5 w-5" /> {t("call")}
      </a>
    </>
  );
}

function ListScreen({ t, lang, go, group }: P & { group: "safety" | "hr" }) {
  return (
    <>
      <Header title={group === "safety" ? t("lessons") : t("hr")} go={go} />
      <div className="grid grid-cols-2 gap-3">
        {TOPICS.filter((x) => x.group === group).map((x, i) => (
          <Tile key={x.id} icon={ICONS[x.icon]} tone={i === 0 ? "primary" : "card"} label={pick(x.title, lang)} onClick={() => go({ s: "lesson", id: x.id })} />
        ))}
      </div>
    </>
  );
}

function Progress({ n, of }: { n: number; of: number }) {
  return (
    <div className="mb-4 flex gap-1.5">
      {Array.from({ length: of }).map((_, i) => <div key={i} className={`bar-track flex-1 ${i <= n ? "bg-secondary" : ""}`} />)}
    </div>
  );
}

function LessonScreen({ t, lang, go, topic }: P & { topic: Topic }) {
  const [i, setI] = useState(0);
  const step = topic.steps[i]!;
  const I = ICONS[step.icon];
  const text = pick(step.text, lang);
  const last = i === topic.steps.length - 1;
  useEffect(() => { speak(text, lang); }, [i]);
  return (
    <>
      <Header title={pick(topic.title, lang)} go={go} />
      <Progress n={i} of={topic.steps.length} />
      <div className="chunky rounded-2xl bg-card p-5">
        <div className="mb-4 grid h-20 w-20 place-items-center rounded-2xl bg-primary"><I className="h-11 w-11" strokeWidth={2.2} /></div>
        <div className="text-xs font-semibold text-muted-foreground">{t("step")} {i + 1}</div>
        <p className="mb-4 mt-1 text-xl font-bold leading-snug">{text}</p>
        <ListenBtn text={text} label={t("listen")} lang={lang} />
      </div>
      <div className="mt-5 flex gap-3">
        {i > 0 && <BigBtn tone="card" className="w-1/3" onClick={() => setI(i - 1)}>{t("back")}</BigBtn>}
        <BigBtn onClick={() => (last ? go({ s: "quiz", id: topic.id }) : setI(i + 1))}>{last ? t("startQ") : t("next")}</BigBtn>
      </div>
    </>
  );
}

function QuizScreen({ t, lang, go, topic }: P & { topic: Topic }) {
  const [qi, setQi] = useState(0);
  const [picked, setPicked] = useState<number | null>(null);
  const [listening, setListening] = useState(false);
  const q = topic.quiz[qi]!;
  const qText = pick(q.q, lang);
  useEffect(() => { speak(qText, lang); }, [qi]);

  const choose = (o: number) => {
    if (picked !== null) return;
    setPicked(o);
    const ok = o === q.answer;
    store.addAttempt({ lang, topic: topic.id, q: qi, correct: ok, at: Date.now() });
    speak(`${ok ? tr("correct", lang) : tr("wrong", lang)} ${pick(q.explain, lang)}`, lang);
  };
  const voice = () => {
    setListening(true);
    listen(lang, (txt) => {
      const n = txt.match(/\d/)?.[0] ?? (/one|first|एक/.test(txt) ? "1" : /two|second|दो/.test(txt) ? "2" : /three|third|तीन/.test(txt) ? "3" : null);
      if (n && +n <= q.options.length) choose(+n - 1);
    }, () => setListening(false));
  };
  const next = () => {
    if (qi < topic.quiz.length - 1) { setQi(qi + 1); setPicked(null); } else go({ s: "done", id: topic.id });
  };

  return (
    <>
      <Header title={pick(topic.title, lang)} go={go} />
      <div className="text-xs font-semibold text-muted-foreground">{qi + 1} / {topic.quiz.length}</div>
      <h2 className="mb-3 mt-1 text-xl font-bold leading-snug">{qText}</h2>
      <div className="mb-4 flex gap-2">
        <ListenBtn text={qText} label={t("listen")} lang={lang} />
        <button onClick={voice} className="chunky inline-flex items-center gap-1.5 rounded-full bg-card px-3 py-1.5 text-sm font-semibold">
          <Mic className="h-4 w-4" /> {listening ? t("listening") : "1 / 2 / 3"}
        </button>
      </div>
      <div className="space-y-3">
        {q.options.map((o, i) => {
          const state = picked === null ? "" : i === q.answer ? "bg-success text-success-foreground" : i === picked ? "bg-destructive text-destructive-foreground" : "opacity-50";
          return (
            <button key={i} onClick={() => choose(i)} className={`chunky flex w-full items-center justify-between rounded-2xl bg-card p-4 text-left font-semibold ${state}`}>
              <span><span className="mr-2 font-display">{i + 1}</span>{pick(o, lang)}</span>
              {picked !== null && i === q.answer && <Check className="h-5 w-5" />}
              {picked === i && i !== q.answer && <X className="h-5 w-5" />}
            </button>
          );
        })}
      </div>
      {picked !== null && (
        <>
          <p className="mt-4 rounded-2xl bg-muted p-4 text-sm"><b>{picked === q.answer ? t("correct") : t("wrong")}</b> {pick(q.explain, lang)}</p>
          <BigBtn onClick={next} className="mt-4">{t("next")}</BigBtn>
        </>
      )}
    </>
  );
}

function DoneScreen({ t, lang, go, topic }: P & { topic: Topic }) {
  useEffect(() => { speak(`${tr("done", lang)}. ${pick(topic.title, lang)}`, lang); }, []);
  return (
    <>
      <div className="chunky mb-6 flex flex-col items-center rounded-2xl bg-primary p-8 text-center text-primary-foreground">
        <Star className="mb-3 h-16 w-16 fill-current" />
        <div className="font-display text-2xl">{t("done")}</div>
        <div className="mt-1 font-semibold">{pick(topic.title, lang)}</div>
      </div>
      <FeedbackScreen t={t} lang={lang} go={go} topicId={topic.id} title={t("clearQ")} />
    </>
  );
}

function FeedbackScreen({ t, lang, go, topicId, title }: P & { topicId: string; title: string }) {
  const [clarity, setClarity] = useState<Feedback["clarity"] | null>(null);
  const [comment, setComment] = useState("");
  const [sent, setSent] = useState(false);
  const [listening, setListening] = useState(false);
  if (sent) return (
    <>
      <p className="chunky rounded-2xl bg-success p-5 text-center font-bold text-success-foreground">{t("thanks")}</p>
      <BigBtn className="mt-4" onClick={() => go({ s: "home" })}><Home className="h-5 w-5" /> {t("home")}</BigBtn>
    </>
  );
  const opts: { k: Feedback["clarity"]; I: LucideIcon }[] = [{ k: "clear", I: ThumbsUp }, { k: "confusing", I: Frown }, { k: "irrelevant", I: Ban }];
  return (
    <>
      <Header title={title} go={go} />
      <div className="grid grid-cols-3 gap-3">
        {opts.map(({ k, I }) => (
          <button key={k} onClick={() => setClarity(k)} className={`chunky flex flex-col items-center gap-2 rounded-2xl p-4 text-sm font-bold ${clarity === k ? "bg-primary text-primary-foreground" : "bg-card"}`}>
            <I className="h-8 w-8" /> {t(k)}
          </button>
        ))}
      </div>
      <div className="mt-4 flex gap-2">
        <input value={comment} onChange={(e) => setComment(e.target.value)} placeholder={t("comment")} className="chunky min-w-0 flex-1 rounded-2xl bg-card px-4 py-3 text-sm" />
        <button aria-label="Speak comment" onClick={() => { setListening(true); listen(lang, (x) => setComment(x), () => setListening(false)); }} className={`chunky grid w-14 place-items-center rounded-2xl ${listening ? "bg-destructive text-destructive-foreground" : "bg-secondary text-secondary-foreground"}`}>
          <Mic className="h-5 w-5" />
        </button>
      </div>
      <BigBtn className="mt-4" onClick={() => { if (!clarity) return; store.addFeedback({ lang, topic: topicId, clarity, comment: comment || undefined, at: Date.now() }); setSent(true); }}>
        {t("send")}
      </BigBtn>
    </>
  );
}

function AnnScreen({ t, lang, go }: P) {
  const anns = useMemo(() => store.announcements(), []);
  const [checking, setChecking] = useState<string | null>(null);
  const [answer, setAnswer] = useState<boolean | null>(null);
  return (
    <>
      <Header title={t("announcements")} go={go} />
      {anns.length === 0 && <p className="text-muted-foreground">{t("noAnn")}</p>}
      <div className="space-y-4">
        {anns.map((a) => (
          <div key={a.id} className="chunky rounded-2xl bg-card p-4">
            <div className="mb-2 text-xs font-semibold text-muted-foreground">{new Date(a.at).toLocaleDateString()}</div>
            <ul className="mb-3 list-disc space-y-1 pl-5 font-semibold">{a.bullets.map((b, i) => <li key={i}>{b}</li>)}</ul>
            <div className="flex flex-wrap gap-2">
              <ListenBtn text={a.bullets.join(". ")} label={t("listen")} lang={lang} />
              <button onClick={() => { setChecking(a.id); setAnswer(null); }} className="chunky rounded-full bg-card px-3 py-1.5 text-sm font-semibold">{t("check")}</button>
            </div>
            {checking === a.id && (
              <div className="mt-4 rounded-xl bg-muted p-3">
                <p className="mb-2 font-semibold">“{a.bullets[0]}” — did you understand this?</p>
                <div className="flex gap-2">
                  {[true, false].map((v) => (
                    <button key={String(v)} onClick={() => { setAnswer(v); store.addAttempt({ lang, topic: "announcement", q: 0, correct: v, at: Date.now() }); }} className={`chunky flex-1 rounded-xl py-2 font-bold ${answer === v ? "bg-primary text-primary-foreground" : "bg-card"}`}>
                      {v ? "Yes / हाँ" : "No / नहीं"}
                    </button>
                  ))}
                </div>
                {answer === false && <p className="mt-2 text-sm">Your supervisor will explain this again. 👍</p>}
              </div>
            )}
          </div>
        ))}
      </div>
    </>
  );
}

const PIN = "1234";

function SupervisorScreen({ go }: { go: (s: Screen) => void }) {
  const [ok, setOk] = useState(false);
  const [pin, setPin] = useState("");
  const [tab, setTab] = useState<"ann" | "stats">("stats");
  const [raw, setRaw] = useState("");
  const [bullets, setBullets] = useState<string[]>([]);
  const [published, setPublished] = useState(false);

  if (!ok) return (
    <>
      <Header title="Supervisor" go={go} />
      <p className="mb-3 text-sm text-muted-foreground">Enter PIN (demo PIN: 1234)</p>
      <input type="password" inputMode="numeric" value={pin} onChange={(e) => setPin(e.target.value)} className="chunky mb-4 w-full rounded-2xl bg-card px-4 py-3 text-2xl tracking-widest" />
      <BigBtn onClick={() => (pin === PIN ? setOk(true) : alert("Wrong PIN"))}>Unlock</BigBtn>
    </>
  );

  const attempts = store.attempts();
  const fb = store.feedback();
  const topicName = (id: string) => TOPICS.find((x) => x.id === id)?.title.en ?? id;
  const groups = new Map<string, { lang: Lang; topic: string; total: number; wrong: number }>();
  attempts.forEach((a) => {
    const k = `${a.topic}|${a.lang}`;
    const g = groups.get(k) ?? { lang: a.lang, topic: a.topic, total: 0, wrong: 0 };
    g.total++; if (!a.correct) g.wrong++;
    groups.set(k, g);
  });
  const rows = [...groups.values()].sort((a, b) => b.wrong / b.total - a.wrong / a.total);

  return (
    <>
      <Header title="Supervisor" go={go} />
      <div className="mb-4 grid grid-cols-2 gap-2">
        <button onClick={() => setTab("stats")} className={`chunky rounded-xl py-2 font-bold ${tab === "stats" ? "bg-primary" : "bg-card"}`}>Analytics</button>
        <button onClick={() => setTab("ann")} className={`chunky rounded-xl py-2 font-bold ${tab === "ann" ? "bg-primary" : "bg-card"}`}>Announcements</button>
      </div>
      {tab === "stats" ? (
        <div className="space-y-4">
          <div className="grid grid-cols-3 gap-2 text-center">
            <Stat n={attempts.length} label="Answers" />
            <Stat n={attempts.length ? Math.round((attempts.filter((a) => a.correct).length / attempts.length) * 100) : 0} label="% correct" />
            <Stat n={fb.length} label="Feedback" />
          </div>
          <section className="chunky rounded-2xl bg-card p-4">
            <h3 className="mb-3 font-bold">Most misunderstood (topic · language)</h3>
            {rows.length === 0 && <p className="text-sm text-muted-foreground">No quiz data yet. Complete a lesson first.</p>}
            {rows.map((r) => {
              const pct = Math.round((r.wrong / r.total) * 100);
              return (
                <div key={r.topic + r.lang} className="mb-3">
                  <div className="flex justify-between text-sm font-semibold"><span>{topicName(r.topic)} · {LANGS.find((l) => l.code === r.lang)?.name}</span><span>{pct}% wrong</span></div>
                  <div className="bar-track mt-1"><div className="h-full rounded-full bg-destructive" style={{ width: `${pct}%` }} /></div>
                </div>
              );
            })}
          </section>
          <section className="chunky rounded-2xl bg-card p-4">
            <h3 className="mb-3 font-bold">Clarity feedback</h3>
            <div className="grid grid-cols-3 gap-2 text-center text-sm">
              {(["clear", "confusing", "irrelevant"] as const).map((c) => <div key={c} className="rounded-xl bg-muted p-2"><div className="font-display text-xl">{fb.filter((f) => f.clarity === c).length}</div>{c}</div>)}
            </div>
            <ul className="mt-3 space-y-1 text-sm">
              {fb.filter((f) => f.comment).slice(-5).reverse().map((f, i) => <li key={i}>“{f.comment}” <span className="text-muted-foreground">— {topicName(f.topic)}, {f.lang}</span></li>)}
            </ul>
          </section>
          <p className="text-xs text-muted-foreground">All data is anonymous. No names or worker IDs are stored.</p>
        </div>
      ) : (
        <div className="space-y-3">
          <textarea value={raw} onChange={(e) => { setRaw(e.target.value); setPublished(false); }} rows={6} placeholder="Paste today's full announcement…" className="chunky w-full rounded-2xl bg-card p-4 text-sm" />
          <BigBtn tone="dark" onClick={() => setBullets(summarize(raw))}>Summarize</BigBtn>
          {bullets.length > 0 && (
            <>
              {bullets.map((b, i) => (
                <input key={i} value={b} onChange={(e) => setBullets(bullets.map((x, j) => (j === i ? e.target.value : x)))} className="chunky w-full rounded-xl bg-card px-3 py-2 text-sm font-semibold" />
              ))}
              <BigBtn onClick={() => { store.addAnnouncement({ id: crypto.randomUUID(), raw, bullets: bullets.filter(Boolean), at: Date.now() }); setPublished(true); }}>
                {published ? "Published ✓" : "Publish to workers"}
              </BigBtn>
            </>
          )}
        </div>
      )}
    </>
  );
}

function Stat({ n, label }: { n: number; label: string }) {
  return <div className="chunky rounded-xl bg-card p-3"><div className="font-display text-2xl">{n}</div><div className="text-xs font-semibold text-muted-foreground">{label}</div></div>;
}
