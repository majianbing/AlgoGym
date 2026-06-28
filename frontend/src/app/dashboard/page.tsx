import { AppShell } from "@/components/AppShell";
import { DashboardClient } from "@/components/DashboardClient";

export default function DashboardPage() {
  return (
    <AppShell eyebrow="Dashboard" title="Today’s workout and streak progress.">
      <DashboardClient />
    </AppShell>
  );
}
