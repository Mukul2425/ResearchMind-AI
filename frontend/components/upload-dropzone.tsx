"use client";

import { UploadCloud } from "lucide-react";
import { motion } from "framer-motion";

export function UploadDropzone() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: "easeOut" }}
      className="rounded-xl2 border-2 border-dashed border-moss/40 bg-canvas/80 p-10 text-center shadow-panel"
    >
      <UploadCloud className="mx-auto mb-4 h-10 w-10 text-moss" />
      <h3 className="text-xl font-semibold">Drop your paper here</h3>
      <p className="mx-auto mt-2 max-w-xl text-sm text-ink/70">
        Step 2 UI shell: wire this to /api/documents/upload in the next commit to start ingestion.
      </p>
      <button
        type="button"
        className="mt-6 rounded-lg bg-ink px-5 py-2 text-sm font-semibold text-canvas transition hover:bg-moss"
      >
        Select PDF
      </button>
    </motion.div>
  );
}
