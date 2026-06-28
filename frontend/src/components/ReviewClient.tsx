"use client";

import { useEffect, useState } from "react";
import { apiRequest, type ReviewData } from "@/lib/api";

export function ReviewClient() {
  const [review, setReview] = useState<ReviewData | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    apiRequest<ReviewData>("/api/review").then(setReview).catch((err: Error) => setError(err.message));
  }, []);

  return (
    <div className="grid gap-5 lg:grid-cols-2">
      {error ? <p className="rounded-md border border-amber-500/40 bg-amber-500/10 p-3 text-amber-200 lg:col-span-2">{error}</p> : null}
      <section className="rounded-lg border border-line bg-panel p-5">
        <h2 className="mb-4 text-xl font-semibold">Due Reviews</h2>
        <div className="grid gap-3">
          {review?.due_sessions.map((item) => (
            <article className="rounded-md border border-line bg-slate-950/40 p-4" key={item.id}>
              <h3 className="font-semibold text-white">{item.problem?.title ?? `Session ${item.id}`}</h3>
              <p className="text-sm text-slate-400">Status: {item.status} · Due: {item.review_due}</p>
            </article>
          ))}
          {review?.due_sessions.length === 0 ? <p className="text-slate-400">No reviews due today.</p> : null}
        </div>
      </section>
      <section className="rounded-lg border border-line bg-panel p-5">
        <h2 className="mb-4 text-xl font-semibold">Weak Patterns</h2>
        <div className="grid gap-3">
          {review?.weak_patterns.map((item) => (
            <article className="rounded-md border border-line bg-slate-950/40 p-4" key={item.pattern}>
              <h3 className="font-semibold text-white">{item.pattern}</h3>
              <p className="text-sm text-slate-400">{item.failures} failures · weak: {String(item.is_weak)}</p>
            </article>
          ))}
          {review?.weak_patterns.length === 0 ? <p className="text-slate-400">No weak patterns marked yet.</p> : null}
        </div>
      </section>
    </div>
  );
}
