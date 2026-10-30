import { createFileRoute } from "@tanstack/react-router";
import { SurakshaApp } from "@/components/SurakshaApp";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "SurakshaTalk — Multilingual Safety Assistant" },
      { name: "description", content: "Voice-first safety lessons, quizzes and announcements for factory workers in Hindi, Kannada, Telugu, Tamil and Bengali." },
      { property: "og:title", content: "SurakshaTalk — Multilingual Safety Assistant" },
      { property: "og:description", content: "Voice-first safety lessons and quizzes for factory workers in their own language." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: SurakshaApp,
});
