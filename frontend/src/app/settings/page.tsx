import { AppShell } from "@/components/AppShell";
import { SettingsClient } from "@/components/SettingsClient";

export default function SettingsPage() {
  return (
    <AppShell eyebrow="Settings" title="Configure local models and storage.">
      <SettingsClient />
    </AppShell>
  );
}
