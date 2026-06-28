import { AppShell } from "@/components/AppShell";
import { KnowledgeClient } from "@/components/KnowledgeClient";

export default function KnowledgeBasePage() {
  return (
    <AppShell eyebrow="Knowledge base" title="Upload markdown notes and ingest them locally.">
      <KnowledgeClient />
    </AppShell>
  );
}
