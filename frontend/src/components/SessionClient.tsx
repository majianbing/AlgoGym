"use client";

import { useEffect, useState } from "react";
import { apiRequest, type PracticeSession, type Today } from "@/lib/api";

export function SessionClient() {
  const [today, setToday] = useState<Today | null>(null);
  const [session, setSession] = useState<PracticeSession | null>(null);
  const [seconds, setSeconds] = useState(0);
  const [hint, setHint] = useState("");
  const [notes, setNotes] = useState("");
  const [hintLevel, setHintLevel] = useState(0);

  useEffect(() => {
    apiRequest<Today>("/api/today").then((data) => {
      setToday(data);
      setSession(data.session);
    });
  }, []);

  useEffect(() => {
    if (!session || session.status !== "in_progress") return;
    const timer = window.setInterval(() => setSeconds((value) => value + 1), 1000);
    return () => window.clearInterval(timer);
  }, [session]);

  async function start() {
    if (!today?.problem) return;
    const started = await apiRequest<PracticeSession>("/api/sessions/start", {
      method: "POST",
      body: JSON.stringify({ problem_id: today.problem.id }),
    });
    setSession(started);
    setSeconds(0);
  }

  async function requestHint(level: number) {
    if (!today?.problem) return;
    setHintLevel(Math.max(hintLevel, level));
    const response = await apiRequest<{ hint: string }>("/api/hints", {
      method: "POST",
      body: JSON.stringify({ problem_id: today.problem.id, level, current_attempt: notes, unlock_solution: false }),
    });
    setHint(response.hint);
  }

  async function finish(status: "solved" | "failed") {
    if (!session) return;
    const finished = await apiRequest<PracticeSession>(`/api/sessions/${session.id}/finish`, {
      method: "POST",
      body: JSON.stringify({
        status,
        time_spent_mins: Math.ceil(seconds / 60),
        notes,
        hint_level_used: hintLevel,
      }),
    });
    setSession(finished);
  }

  return (
    <div className="grid gap-5 lg:grid-cols-[1fr_420px]">
      <section className="rounded-lg border border-line bg-panel p-5">
        <h2 className="text-2xl font-semibold text-white">{today?.problem?.title ?? "Loading problem"}</h2>
        <p className="mb-4 text-slate-400">{today?.problem?.difficulty} · {today?.problem?.pattern}</p>
        <p className="mb-5 rounded-md border border-line bg-slate-950/50 p-4 text-slate-300">{today?.problem?.prompt}</p>
        <div className="mb-5 text-4xl font-bold text-mint">{Math.floor(seconds / 60)}:{String(seconds % 60).padStart(2, "0")}</div>
        {!session ? (
          <button className="rounded-md bg-mint px-4 py-2 font-bold text-slate-950" onClick={start}>Start timer</button>
        ) : (
          <div className="flex gap-3">
            <button className="rounded-md bg-emerald-400 px-4 py-2 font-bold text-slate-950" onClick={() => finish("solved")}>Finish solved</button>
            <button className="rounded-md bg-rose-400 px-4 py-2 font-bold text-slate-950" onClick={() => finish("failed")}>Finish failed</button>
          </div>
        )}
      </section>
      <aside className="grid gap-4 rounded-lg border border-line bg-panel p-5">
        <label className="grid gap-2 text-sm text-slate-300">
          Notes / current attempt
          <textarea className="min-h-32 rounded-md border border-line bg-slate-950 p-3" value={notes} onChange={(event) => setNotes(event.target.value)} />
        </label>
        <div className="grid grid-cols-3 gap-2">
          {[1, 2, 3].map((level) => (
            <button className="rounded-md bg-slate-800 px-3 py-2 text-sm font-bold text-mint" key={level} onClick={() => requestHint(level)}>
              Hint {level}
            </button>
          ))}
        </div>
        {hint ? <pre className="rounded-md border border-line bg-slate-950 p-3 text-sm text-slate-200">{hint}</pre> : null}
      </aside>
    </div>
  );
}
