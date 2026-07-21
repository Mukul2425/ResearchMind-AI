import { Sidebar } from "@/components/sidebar";
import { UploadDropzone } from "@/components/upload-dropzone";

export default function UploadPage() {
  return (
    <main className="mx-auto min-h-screen max-w-7xl px-5 py-6 md:px-8">
      <div className="grid gap-6 md:grid-cols-[240px_1fr]">
        <Sidebar />
        <section className="space-y-4">
          <header className="rounded-xl2 border border-ink/10 bg-canvas/90 p-6 shadow-panel">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-ember">Document Upload</p>
            <h1 className="mt-2 text-3xl font-bold">Bring papers into ResearchMind</h1>
            <p className="mt-2 text-sm text-ink/80">
              Upload now sends PDFs to backend ingestion and returns a trackable document ID.
            </p>
          </header>
          <UploadDropzone />
        </section>
      </div>
    </main>
  );
}
