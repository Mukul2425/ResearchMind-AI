"use client";

import { UploadCloud } from "lucide-react";
import { motion } from "framer-motion";
import { useRef, useState } from "react";

import { uploadPdf, type UploadResponse } from "@/lib/api";

export function UploadDropzone() {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null);
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const triggerPicker = () => fileInputRef.current?.click();

  const onFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (file.type !== "application/pdf") {
      setError("Please select a PDF file.");
      setUploadResult(null);
      return;
    }

    setSelectedFileName(file.name);
    setIsUploading(true);
    setError(null);
    setUploadResult(null);

    try {
      const result = await uploadPdf(file);
      setUploadResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: "easeOut" }}
      className="rounded-xl2 border-2 border-dashed border-moss/40 bg-canvas/80 p-10 text-center shadow-panel"
    >
      <input
        ref={fileInputRef}
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={onFileSelect}
      />

      <UploadCloud className="mx-auto mb-4 h-10 w-10 text-moss" />
      <h3 className="text-xl font-semibold">Drop your paper here</h3>
      <p className="mx-auto mt-2 max-w-xl text-sm text-ink/70">
        Uploads are now wired to backend ingestion endpoint and return a document ID for pipeline tracking.
      </p>
      <button
        type="button"
        onClick={triggerPicker}
        disabled={isUploading}
        className="mt-6 rounded-lg bg-ink px-5 py-2 text-sm font-semibold text-canvas transition hover:bg-moss"
      >
        {isUploading ? "Uploading..." : "Select PDF"}
      </button>

      {selectedFileName ? <p className="mt-3 text-xs text-ink/70">Selected: {selectedFileName}</p> : null}

      {uploadResult ? (
        <div className="mx-auto mt-4 max-w-xl rounded-lg border border-moss/30 bg-moss/10 p-3 text-left text-sm">
          <p className="font-semibold text-moss">Upload complete</p>
          <p className="mt-1 text-ink">File: {uploadResult.filename}</p>
          <p className="mt-1 break-all text-ink/80">Document ID: {uploadResult.document_id}</p>
        </div>
      ) : null}

      {error ? <p className="mt-4 text-sm font-medium text-ember">{error}</p> : null}
    </motion.div>
  );
}
