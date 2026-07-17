import { Sidebar } from "@/components/sidebar";

export default function LibraryPage() {
  return (
    <main className="mx-auto min-h-screen max-w-7xl px-5 py-6 md:px-8">
      <div className="grid gap-6 md:grid-cols-[240px_1fr]">
        <Sidebar />
        <section className="rounded-xl2 border border-ink/10 bg-canvas/90 p-6 shadow-panel">
          <h1 className="text-2xl font-bold">Library</h1>
          <p className="mt-2 text-sm text-ink/75">Document cards and metadata browser will be added in upcoming steps.</p>
        </section>
      </div>
    </main>
  );
}
