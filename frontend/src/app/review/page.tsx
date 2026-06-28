import { AppShell } from "@/components/AppShell";
import { ReviewClient } from "@/components/ReviewClient";

export default function ReviewPage() {
  return (
    <AppShell eyebrow="Review" title="Convert mistakes into pattern mastery.">
      <ReviewClient />
    </AppShell>
  );
}
