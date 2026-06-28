import { AppShell } from "@/components/AppShell";
import { SessionClient } from "@/components/SessionClient";

export default function SessionPage() {
  return (
    <AppShell eyebrow="Session" title="Start a timer, request tiered hints, and finish practice.">
      <SessionClient />
    </AppShell>
  );
}
