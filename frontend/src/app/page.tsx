"use client";

import { useEffect, useMemo, useState } from "react";

type Plugin = { id: string; name: string; capabilities: string[] };
type Dataset = { id: string; name: string; description: string; document_count: number; test_count: number; capabilities: string[] };
type Run = {
  id: string;
  plugin_id: string;
  dataset_id: string;
  status: string;
  result: { summary: { score: number; retrieval_recall: number; citation_recall: number; average_latency_ms: number; test_count: number; evaluator: string }; cases: Array<{ id: string; question: string; answer: string; retrieved_document_ids: string[]; expected_document_ids: string[]; trace: Record<string, unknown> }> };
};

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export default function HomePage() {
  const [plugins, setPlugins] = useState<Plugin[]>([]);
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [runs, setRuns] = useState<Run[]>([]);
  const [pluginId, setPluginId] = useState("simple");
  const [datasetId, setDatasetId] = useState("starter-rag");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const selectedRun = runs[0];

  useEffect(() => {
    Promise.all([fetch(`${apiUrl}/benchmark/plugins`), fetch(`${apiUrl}/benchmark/datasets`), fetch(`${apiUrl}/benchmark/runs`)])
      .then(async ([pluginResponse, datasetResponse, runResponse]) => {
        if (!pluginResponse.ok || !datasetResponse.ok || !runResponse.ok) throw new Error("Could not reach the benchmark API.");
        const [pluginData, datasetData, runData] = await Promise.all([pluginResponse.json(), datasetResponse.json(), runResponse.json()]);
        setPlugins(pluginData); setDatasets(datasetData); setRuns(runData);
      })
      .catch((reason: Error) => setError(reason.message));
  }, []);

  const selectedPlugin = useMemo(() => plugins.find((plugin) => plugin.id === pluginId), [pluginId, plugins]);

  async function startRun() {
    setLoading(true); setError("");
    try {
      const response = await fetch(`${apiUrl}/benchmark/runs`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ plugin_id: pluginId, dataset_id: datasetId, top_k: 3 }) });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail ?? "Benchmark run failed.");
      setRuns((current) => [body, ...current]);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Benchmark run failed.");
    } finally { setLoading(false); }
  }

  return <main className="min-h-screen bg-slate-950 text-slate-100">
    <div className="mx-auto max-w-7xl px-6 py-12">
      <header className="mb-10 flex flex-col justify-between gap-4 border-b border-slate-800 pb-8 md:flex-row md:items-end">
        <div><p className="mb-2 text-sm font-semibold tracking-[0.2em] text-cyan-400">RAG EVALUATION LAB</p><h1 className="text-4xl font-semibold tracking-tight">Compare RAG architectures with evidence.</h1><p className="mt-3 max-w-2xl text-slate-400">A plug-and-play benchmark for retrieval quality, citations, latency, and Giskard-ready evaluation.</p></div>
        <div className="rounded-full border border-cyan-400/30 bg-cyan-400/10 px-4 py-2 text-sm text-cyan-200">Groq + LangChain · Sentence Transformers</div>
      </header>

      <section className="grid gap-5 lg:grid-cols-[1.1fr_1.9fr]">
        <aside className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="text-lg font-semibold">New benchmark run</h2><p className="mt-1 text-sm text-slate-400">Every plugin returns answer, sources, citations, and trace data.</p>
          <label className="mt-6 block text-sm font-medium">RAG implementation<select value={pluginId} onChange={(event) => setPluginId(event.target.value)} className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-sm">{plugins.map((plugin) => <option key={plugin.id} value={plugin.id}>{plugin.name}</option>)}</select></label>
          {selectedPlugin && <div className="mt-3 flex flex-wrap gap-2">{selectedPlugin.capabilities.map((capability) => <span key={capability} className="rounded bg-slate-800 px-2 py-1 text-xs text-slate-300">{capability}</span>)}</div>}
          <label className="mt-5 block text-sm font-medium">Benchmark dataset<select value={datasetId} onChange={(event) => setDatasetId(event.target.value)} className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-sm">{datasets.map((dataset) => <option key={dataset.id} value={dataset.id}>{dataset.name}</option>)}</select></label>
          <button onClick={startRun} disabled={loading || !plugins.length} className="mt-7 w-full rounded-lg bg-cyan-400 px-4 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50">{loading ? "Running…" : "Run benchmark"}</button>
          {error && <p className="mt-4 rounded-lg border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-200">{error}</p>}
        </aside>

        <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
          <div className="flex items-center justify-between"><div><h2 className="text-lg font-semibold">Latest results</h2><p className="mt-1 text-sm text-slate-400">Fixed-suite smoke score. Giskard testset generation is the next evaluation layer.</p></div>{selectedRun && <span className="text-sm text-slate-400">{selectedRun.plugin_id} · {selectedRun.dataset_id}</span>}</div>
          {selectedRun ? <><div className="mt-6 grid gap-3 sm:grid-cols-4"><Metric label="Score" value={`${selectedRun.result.summary.score}%`} strong /><Metric label="Retrieval recall" value={`${Math.round(selectedRun.result.summary.retrieval_recall * 100)}%`} /><Metric label="Citation recall" value={`${Math.round(selectedRun.result.summary.citation_recall * 100)}%`} /><Metric label="Avg. latency" value={`${selectedRun.result.summary.average_latency_ms} ms`} /></div>
          <div className="mt-6 overflow-x-auto"><table className="w-full min-w-[620px] text-left text-sm"><thead className="border-b border-slate-800 text-xs uppercase tracking-wide text-slate-500"><tr><th className="pb-3 pr-4">Question</th><th className="pb-3 pr-4">Retrieved</th><th className="pb-3">Answer</th></tr></thead><tbody>{selectedRun.result.cases.map((item) => <tr key={item.id} className="border-b border-slate-800/70 align-top"><td className="py-4 pr-4 text-slate-300">{item.question}</td><td className="py-4 pr-4"><code className="text-cyan-300">{item.retrieved_document_ids.join(", ")}</code></td><td className="py-4 text-slate-400">{item.answer}</td></tr>)}</tbody></table></div></> : <div className="mt-8 rounded-xl border border-dashed border-slate-700 p-10 text-center text-sm text-slate-500">Select an implementation and run the starter suite. Add <code>GROQ_API_KEY</code> to the backend environment first.</div>}
        </section>
      </section>
    </div>
  </main>;
}

function Metric({ label, value, strong = false }: { label: string; value: string; strong?: boolean }) { return <div className="rounded-xl border border-slate-800 bg-slate-950/70 p-4"><p className="text-xs uppercase tracking-wide text-slate-500">{label}</p><p className={`mt-2 text-2xl ${strong ? "font-semibold text-cyan-300" : "text-slate-100"}`}>{value}</p></div>; }
