"use client";

import { motion } from "framer-motion";

import { Sidebar } from "@/components/sidebar";
import { StatusPill } from "@/components/status-pill";
import { useApiHealth } from "@/hooks/use-api-health";

const metrics = [
  { label: "Uploaded Papers", value: "0", note: "Awaiting ingestion" },
  { label: "Conversations", value: "0", note: "Start your first query" },
  { label: "Cited Answers", value: "0", note: "Grounded responses only" },
];

export default function DashboardPage() {
  const health = useApiHealth();

  return (
    <main className="mx-auto min-h-screen max-w-7xl px-5 py-6 md:px-8">
      <div className="grid gap-6 md:grid-cols-[240px_1fr]">
        <Sidebar />

        <section className="space-y-6">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35, ease: "easeOut" }}
            className="rounded-xl2 border border-ink/10 bg-canvas/90 p-6 shadow-panel"
          >
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-ember">Phase 1 / Step 2</p>
            <h1 className="mt-2 font-[family-name:var(--font-heading)] text-4xl font-bold md:text-5xl">
              Build your living research workspace.
            </h1>
            <p className="mt-3 max-w-2xl text-sm text-ink/80">
              Frontend shell is live. Backend connectivity is checked from this page so your next commits can focus on upload,
              parsing, and retrieval.
            </p>
            <div className="mt-5">
              <StatusPill status={health.status} loading={health.loading} />
              {health.error ? <p className="mt-2 text-xs text-ember">{health.error}</p> : null}
            </div>
          </motion.div>

          <div className="grid gap-4 md:grid-cols-3">
            {metrics.map((metric, idx) => (
              <motion.article
                key={metric.label}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25, delay: idx * 0.08 }}
                className="rounded-xl2 border border-ink/10 bg-canvas/90 p-5 shadow-panel"
              >
                <p className="text-xs uppercase tracking-[0.18em] text-moss">{metric.label}</p>
                <p className="mt-2 text-3xl font-bold text-ink">{metric.value}</p>
                <p className="mt-1 text-sm text-ink/70">{metric.note}</p>
              </motion.article>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
