"use client";

import { FormEvent, useEffect, useState } from "react";
import { apiRequest, type RuntimeSettings } from "@/lib/api";

export function SettingsClient() {
  const [settings, setSettings] = useState<RuntimeSettings | null>(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    apiRequest<RuntimeSettings>("/api/settings").then(setSettings).catch((err: Error) => setMessage(err.message));
  }, []);

  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const updated = await apiRequest<RuntimeSettings>("/api/settings", {
      method: "PUT",
      body: JSON.stringify({
        ollama_base_url: form.get("ollama_base_url"),
        llm_model: form.get("llm_model"),
        embedding_model: form.get("embedding_model"),
        api_key: form.get("api_key"),
      }),
    });
    setSettings(updated);
    setMessage("Settings saved locally.");
  }

  return (
    <div className="grid gap-5 lg:grid-cols-[420px_1fr]">
      <form className="grid gap-4 rounded-lg border border-line bg-panel p-5" onSubmit={save}>
        <h2 className="text-xl font-semibold">Ollama Preferences</h2>
        <label className="grid gap-2 text-sm text-slate-300">
          API base URL
          <input className="rounded-md border border-line bg-slate-950 p-3" name="ollama_base_url" defaultValue={settings?.preferences.ollama_base_url ?? settings?.runtime.ollama_base_url ?? ""} />
        </label>
        <label className="grid gap-2 text-sm text-slate-300">
          Chat model
          <input className="rounded-md border border-line bg-slate-950 p-3" name="llm_model" defaultValue={settings?.preferences.llm_model ?? settings?.runtime.llm_model ?? "llama3.2"} />
        </label>
        <label className="grid gap-2 text-sm text-slate-300">
          Embedding model
          <input className="rounded-md border border-line bg-slate-950 p-3" name="embedding_model" defaultValue={settings?.preferences.embedding_model ?? settings?.runtime.embedding_model ?? "nomic-embed-text"} />
        </label>
        <label className="grid gap-2 text-sm text-slate-300">
          API key
          <input className="rounded-md border border-line bg-slate-950 p-3" name="api_key" defaultValue={settings?.preferences.api_key ?? "ollama"} />
        </label>
        <button className="rounded-md bg-mint px-4 py-2 font-bold text-slate-950">Save settings</button>
        {message ? <p className="text-sm text-slate-300">{message}</p> : null}
      </form>
      <section className="rounded-lg border border-line bg-panel p-5">
        <h2 className="mb-4 text-xl font-semibold">Runtime</h2>
        <div className="grid gap-3 text-sm text-slate-300">
          <p>Ollama: {settings?.runtime.ollama_base_url ?? "unknown"}</p>
          <p>LLM: {settings?.runtime.llm_model ?? "unknown"}</p>
          <p>Embeddings: {settings?.runtime.embedding_model ?? "unknown"}</p>
          <p>Chroma path: {settings?.runtime.chroma_path ?? "unknown"}</p>
        </div>
      </section>
    </div>
  );
}
