interface StatsCardProps {
  label: string;
  value: string;
  accent?: "allow" | "verify" | "review" | "block" | "default";
}

const ACCENT_CLASSES: Record<string, string> = {
  allow: "text-signal-allow",
  verify: "text-signal-verify",
  review: "text-signal-review",
  block: "text-signal-block",
  default: "text-base-200",
};

export default function StatsCard({ label, value, accent = "default" }: StatsCardProps) {
  return (
    <div className="rounded-lg border border-base-700 bg-base-900 px-5 py-4">
      <div className="text-xs uppercase tracking-wide text-base-400">{label}</div>
      <div className={`mt-2 text-2xl font-medium ${ACCENT_CLASSES[accent]}`}>{value}</div>
    </div>
  );
}
