"use client";

import { FormEvent, useEffect, useState } from "react";
import { apiRequest, type PlanWeek } from "@/lib/api";

export function PlanClient() {
  const [weeks, setWeeks] = useState<PlanWeek[]>([]);
  const [generated, setGenerated] = useState("");

  useEffect(() => {
    apiRequest<PlanWeek[]>("/api/plan").then(setWeeks).catch(() => setWeeks([]));
  }, []);

  async function generate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const response = await apiRequest<{ generated: string; rag_available: boolean }>("/api/plan/generate", {
      method: "POST",
      body: JSON.stringify({ goal: form.get("goal") }),
    });
    setGenerated(response.generated);
  }

  return (
    <div className="grid gap-5">
      <form className="flex flex-col gap-3 rounded-lg border border-line bg-panel p-5 md:flex-row" onSubmit={generate}>
        <input className="min-w-0 flex-1 rounded-md border border-line bg-slate-950 p-3" name="goal" placeholder="Generate a custom plan goal" />
        <button className="rounded-md bg-mint px-4 py-2 font-bold text-slate-950">Generate</button>
      </form>
      {generated ? <pre className="rounded-lg border border-line bg-slate-950 p-4 text-sm text-slate-200">{generated}</pre> : null}
      <section className="grid gap-4 lg:grid-cols-2">
        {weeks.map((week) => (
          <article className="rounded-lg border border-line bg-panel p-5" key={week.week}>
            <h2 className="mb-4 text-xl font-semibold">Week {week.week}</h2>
            <div className="grid gap-3">
              {week.problems.map((problem) => (
                <div className="rounded-md border border-line bg-slate-950/40 p-3" key={problem.id}>
                  <p className="font-semibold text-white">Day {problem.day}: {problem.title}</p>
                  <p className="text-sm text-slate-400">{problem.difficulty} · {problem.pattern}</p>
                </div>
              ))}
            </div>
          </article>
        ))}
      </section>
    </div>
  );
}
