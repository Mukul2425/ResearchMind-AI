import { Activity } from "lucide-react";

type StatusPillProps = {
  status: string;
  loading?: boolean;
};

export function StatusPill({ status, loading = false }: StatusPillProps) {
  const tone =
    loading || status === "checking"
      ? "bg-sand/80 text-ink"
      : status === "ok"
      ? "bg-moss text-canvas"
      : "bg-ember text-canvas";

  return (
    <div className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-sm font-medium ${tone}`}>
      <Activity className="h-4 w-4" />
      <span>{loading ? "Connecting" : `API ${status}`}</span>
    </div>
  );
}
