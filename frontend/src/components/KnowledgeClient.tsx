"use client";

import { FormEvent, useEffect, useState } from "react";
import { apiRequest, type DocumentRecord } from "@/lib/api";

export function KnowledgeClient() {
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  function refresh() {
    apiRequest<DocumentRecord[]>("/api/documents").then(setDocuments).catch((err: Error) => setMessage(err.message));
  }

  useEffect(refresh, []);

  async function upload(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setMessage("");
    const form = new FormData(event.currentTarget);
    try {
      const doc = await apiRequest<DocumentRecord>("/api/documents/upload", { method: "POST", body: form });
      await apiRequest<DocumentRecord>(`/api/documents/${doc.id}/ingest`, { method: "POST" });
      event.currentTarget.reset();
      refresh();
      setMessage("Document uploaded, chunked by ## headings, and embedded into ChromaDB.");
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid gap-5 lg:grid-cols-[420px_1fr]">
      <form className="grid gap-4 rounded-lg border border-line bg-panel p-5" onSubmit={upload}>
        <h2 className="text-xl font-semibold">Markdown Upload</h2>
        <label className="grid gap-2 text-sm text-slate-300">
          Document
          <input className="rounded-md border border-line bg-slate-950 p-3" name="file" type="file" accept=".md,.markdown" required />
        </label>
        <button className="rounded-md bg-mint px-4 py-2 font-bold text-slate-950" disabled={loading}>
          {loading ? "Ingesting..." : "Upload and ingest"}
        </button>
        {message ? <p className="text-sm text-slate-300">{message}</p> : null}
      </form>
      <section className="rounded-lg border border-line bg-panel p-5">
        <h2 className="mb-4 text-xl font-semibold">Ingested Documents</h2>
        <div className="grid gap-3">
          {documents.map((doc) => (
            <article className="rounded-md border border-line bg-slate-950/40 p-4" key={doc.id}>
              <div className="flex justify-between gap-3">
                <h3 className="font-semibold text-white">{doc.filename}</h3>
                <span className="text-sm text-mint">{doc.chunks_count} chunks</span>
              </div>
              <p className="text-sm text-slate-400">chunked: {String(doc.chunked)} · embedded: {String(doc.embedded)}</p>
            </article>
          ))}
          {documents.length === 0 ? <p className="text-slate-400">No documents yet.</p> : null}
        </div>
      </section>
    </div>
  );
}
