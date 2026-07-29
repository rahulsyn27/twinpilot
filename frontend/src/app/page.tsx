import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center p-8">
      <section className="w-full max-w-xl rounded-lg border p-6 shadow-sm">
        <h1 className="mb-3 text-2xl font-semibold">TwinPilot Platform</h1>
        <p className="mb-6 text-sm text-slate-600">
          Frontend foundation is ready and connected to the backend API surface.
        </p>
        <Button>Foundation Ready</Button>
      </section>
    </main>
  );
}
