"use client";

import { useEffect, useState } from "react";
import { apiRequest, type Stats, type Today } from "@/lib/api";

export function DashboardClient() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [today, setToday] = useState<Today | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([apiRequest<Stats>("/api/stats"), apiRequest<Today>("/api/today")])
      .then(([statsData, todayData]) => {
        setStats(statsData);
        setToday(todayData);
      })
      .catch((err: Error) => setError(err.message));
  }, []);

  return (
    <div className="grid gap-5">
      {error ? <p className="rounded-md border border-amber-500/40 bg-amber-500/10 p-3 text-amber-200">{error}</p> : null}
      <section className="grid gap-4 md:grid-cols-4">
        <Metric label="Current streak" value={`${stats?.current_streak ?? 0} days`} />
        <Metric label="Longest streak" value={`${stats?.longest_streak ?? 0} days`} />
        <Metric label="Solved" value={`${stats?.solved_sessions ?? 0}`} />
        <Metric label="Documents" value={`${stats?.documents ?? 0}`} />
      </section>
      <section className="rounded-lg border border-line bg-panel p-5">
        <div className="mb-4 flex items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-semibold text-white">{today?.problem?.title ?? "Loading workout"}</h2>
            <p className="text-sm text-slate-400">
              {today?.problem ? `${today.problem.difficulty} · ${today.problem.pattern}` : "Seed data powers this before RAG is configured."}
            </p>
          </div>
          <a href="/session" className="rounded-md bg-mint px-4 py-2 text-sm font-bold text-slate-950">
            Start session
          </a>
        </div>
        <div className="grid gap-3 md:grid-cols-4">
          {today?.workout
            ? Object.entries(today.workout).map(([key, value]) => (
                <article className="rounded-md border border-line bg-slate-950/40 p-4" key={key}>
                  <h3 className="mb-2 text-sm font-bold capitalize text-mint">{key.replace("_", " ")}</h3>
                  <p className="text-sm text-slate-300">{value}</p>
                </article>
              ))
            : null}
        </div>
      </section>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <article className="rounded-lg border border-line bg-panel p-5">
      <p className="mb-2 text-sm text-slate-400">{label}</p>
      <strong className="text-2xl text-white">{value}</strong>
    </article>
  );
}
