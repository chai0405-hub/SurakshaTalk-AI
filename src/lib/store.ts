// Anonymous on-device storage: quiz attempts, clarity feedback, announcements.
// No names or IDs of workers are ever saved.
import type { Lang } from "./content";

export type Attempt = { lang: Lang; topic: string; q: number; correct: boolean; at: number };
export type Feedback = { lang: Lang; topic: string; clarity: "clear" | "confusing" | "irrelevant"; comment?: string | undefined; at: number };
export type Announcement = { id: string; raw: string; bullets: string[]; at: number };

const get = <X>(k: string, d: X): X => {
  if (typeof window === "undefined") return d;
  try { return JSON.parse(localStorage.getItem(k) ?? "") as X; } catch { return d; }
};
const set = (k: string, v: unknown) => localStorage.setItem(k, JSON.stringify(v));

export const store = {
  attempts: () => get<Attempt[]>("st.attempts", []),
  addAttempt: (a: Attempt) => set("st.attempts", [...store.attempts(), a]),
  feedback: () => get<Feedback[]>("st.feedback", []),
  addFeedback: (f: Feedback) => set("st.feedback", [...store.feedback(), f]),
  announcements: () => get<Announcement[]>("st.ann", [DEFAULT_ANN]),
  addAnnouncement: (a: Announcement) => set("st.ann", [a, ...store.announcements()]),
  lang: () => get<Lang>("st.lang", "en"),
  setLang: (l: Lang) => set("st.lang", l),
};

const DEFAULT_ANN: Announcement = {
  id: "seed",
  raw: "",
  bullets: [
    "Tomorrow B-shift starts at 2:00 PM (not 3:00 PM).",
    "Reason: compressor machine repair.",
    "Line 4 workers: wear ear protection all the time.",
  ],
  at: Date.now(),
};

/** Rule-based summarizer: split into sentences, keep the shortest informative ones, max 4 bullets. */
export function summarize(text: string): string[] {
  const sentences = text
    .replace(/\s+/g, " ")
    .split(/(?<=[.!?।])\s+|\n+/)
    .map((s) => s.trim())
    .filter((s) => s.length > 3);
  const filler = /^(dear|hello|hi|good (morning|evening)|thank|regards|please note that)/i;
  return sentences
    .filter((s) => !filler.test(s))
    .map((s) => (s.length > 110 ? s.slice(0, 107).trim() + "…" : s))
    .slice(0, 4);
}
