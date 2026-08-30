"use client";

import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { api, DashboardSummary, Interaction, EvaluateResult } from "@/lib/api";
import StatsCard from "@/components/StatsCard";
import RiskGauge from "@/components/RiskGauge";

const DECISION_LABELS: Record<string, string> = {
  allow: "Allow",
  verify: "Verify / edit",
  human_review: "Human review",
  block: "Block",
};

export default function OverviewPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [interactions, setInteractions] = useState<Interaction[]>([]);
  const [prompt, setPrompt] = useState("");
  const [testing, setTesting] = useState(false);
  const [result, setResult] = useState<EvaluateResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function loadData() {
    try {
      const [s, i] = await Promise.all([api.getSummary(), api.getInteractions()]);
      setSummary(s);
      setInteractions(i);
      setError(null);
    } catch (err) {
      setError("Couldn't reach the ControlPlane API. Is the backend running?");
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleTest() {
    if (!prompt.trim()) return;
    setTesting(true);
    setResult(null);
    try {
      const res = await api.evaluate(prompt);
      setResult(res);
      await loadData();
    } catch (err) {
      setError("Evaluation request failed.");
    } finally {
      setTesting(false);
    }
  }

  const chartData = [...interactions]
    .reverse()
    .map((i, idx) => ({ index: idx + 1, risk: i.risk_score }));

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-xl font-medium text-base-200">Overview</h1>
        <p className="mt-1 text-sm text-base-400">
          Live risk posture across every AI interaction ControlPlane has evaluated.
        </p>
      </div>

      {error && (
        <div className="rounded-md border border-signal-block/40 bg-signal-block/10 px-4 py-3 text-sm text-signal-block">
          {error}
        </div>
      )}

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatsCard label="Total interactions" value={String(summary?.total_interactions ?? 0)} />
        <StatsCard
          label="Avg risk score"
          value={summary ? summary.avg_risk_score.toFixed(1) : "0"}
          accent="verify"
        />
        <StatsCard
          label="Blocked"
          value={String(summary?.blocked_count ?? 0)}
          accent="block"
        />
        <StatsCard
          label="Human review"
          value={String(summary?.human_review_count ?? 0)}
          accent="review"
        />
      </div>

      <div className="rounded-lg border border-base-700 bg-base-900 p-5">
        <h2 className="mb-4 text-sm font-medium text-base-200">Risk score trend</h2>
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#242B34" />
              <XAxis dataKey="index" stroke="#8A94A3" fontSize={12} />
              <YAxis stroke="#8A94A3" fontSize={12} domain={[0, 100]} />
              <Tooltip
                contentStyle={{ background: "#1A1F26", border: "1px solid #333C48", fontSize: 12 }}
              />
              <Line type="monotone" dataKey="risk" stroke="#4AA8E0" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-sm text-base-400">No interactions yet — run a test prompt below.</p>
        )}
      </div>

      <div className="rounded-lg border border-base-700 bg-base-900 p-5">
        <h2 className="mb-3 text-sm font-medium text-base-200">Test a prompt</h2>
        <p className="mb-3 text-sm text-base-400">
          Send a prompt through the full ControlPlane pipeline: routing, fact-checking, privacy
          and safety screening, and risk scoring.
        </p>
        <div className="flex gap-3">
          <input
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleTest()}
            placeholder="e.g. What is our leave policy?"
            className="flex-1 rounded-md border border-base-700 bg-base-800 px-3 py-2 text-sm text-base-200 outline-none focus:border-signal-verify"
          />
          <button
            onClick={handleTest}
            disabled={testing}
            className="rounded-md bg-signal-verify px-4 py-2 text-sm font-medium text-base-950 disabled:opacity-50"
          >
            {testing ? "Evaluating..." : "Evaluate"}
          </button>
        </div>

        {result && (
          <div className="mt-4 space-y-3 rounded-md border border-base-700 bg-base-800 p-4">
            <div className="flex items-center justify-between">
              <span className="text-xs uppercase tracking-wide text-base-400">
                Decision: <span className="text-base-200">{DECISION_LABELS[result.decision]}</span>
              </span>
              <span className="text-xs text-base-400">Model: {result.model_used}</span>
            </div>
            <RiskGauge score={result.risk_score} />
            <p className="text-sm text-base-200">{result.response}</p>
          </div>
        )}
      </div>

      <div className="rounded-lg border border-base-700 bg-base-900 p-5">
        <h2 className="mb-4 text-sm font-medium text-base-200">Recent interactions</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-base-700 text-xs uppercase text-base-400">
                <th className="pb-2 pr-4">Prompt</th>
                <th className="pb-2 pr-4">Model</th>
                <th className="pb-2 pr-4">Risk</th>
                <th className="pb-2">Decision</th>
              </tr>
            </thead>
            <tbody>
              {interactions.slice(0, 10).map((i) => (
                <tr key={i.id} className="border-b border-base-800 text-base-200">
                  <td className="max-w-xs truncate py-2 pr-4">{i.prompt}</td>
                  <td className="py-2 pr-4 text-base-400">{i.model_used}</td>
                  <td className="py-2 pr-4">{i.risk_score}</td>
                  <td className="py-2 text-base-400">{DECISION_LABELS[i.decision]}</td>
                </tr>
              ))}
              {interactions.length === 0 && (
                <tr>
                  <td colSpan={4} className="py-4 text-center text-base-400">
                    No interactions yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
