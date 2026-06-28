import { AppShell } from "@/components/AppShell";
import { PlanClient } from "@/components/PlanClient";

export default function PlanPage() {
  return (
    <AppShell eyebrow="Plan" title="Follow the seeded 6-week curriculum or generate a custom plan.">
      <PlanClient />
    </AppShell>
  );
}
