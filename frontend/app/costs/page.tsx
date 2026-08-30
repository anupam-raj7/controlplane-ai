"use client";

import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { api, DashboardSummary, Interaction } from "@/lib/api";
import StatsCard from "@/components/StatsCard";

export default function CostsPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [interactions, setInteractions] = useState<Interaction[]>([]);

  useEffect(() => {
    api.getSummary().then(setSummary).catch(() => {});
    api.getInteractions().then(setInteractions).catch(() => {});
  }, []);

  const modelData = summary
    ? Object.entries(summary.model_usage).map(([model, count]) => ({ model, count }))
    : [];

  const avgCostPerCall =
    summary && summary.total_interactions > 0
      ? summary.total_cost_usd / summary.total_interactions
      : 0;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-xl font-medium text-base-200">Cost</h1>
        <p className="mt-1 text-sm text-base-400">
          Where AI spend is going, and how the model router is splitting traffic.
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-3">
        <StatsCard label="Total spend" value={`$${(summary?.total_cost_usd ?? 0).toFixed(4)}`} />
        <StatsCard label="Avg cost / call" value={`$${avgCostPerCall.toFixed(5)}`} />
        <StatsCard label="Total calls" value={String(summary?.total_interactions ?? 0)} />
      </div>

      <div className="rounded-lg border border-base-700 bg-base-900 p-5">
        <h2 className="mb-4 text-sm font-medium text-base-200">Requests by model</h2>
        {modelData.length > 0 ? (
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={modelData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#242B34" />
              <XAxis dataKey="model" stroke="#8A94A3" fontSize={12} />
              <YAxis stroke="#8A94A3" fontSize={12} allowDecimals={false} />
              <Tooltip
                contentStyle={{ background: "#1A1F26", border: "1px solid #333C48", fontSize: 12 }}
              />
              <Bar dataKey="count" fill="#4AA8E0" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-sm text-base-400">No requests yet.</p>
        )}
      </div>

      <div className="rounded-lg border border-base-700 bg-base-900 p-5">
        <h2 className="mb-4 text-sm font-medium text-base-200">Per-request cost breakdown</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-base-700 text-xs uppercase text-base-400">
                <th className="pb-2 pr-4">Prompt</th>
                <th className="pb-2 pr-4">Model</th>
                <th className="pb-2 pr-4">Latency</th>
                <th className="pb-2">Cost</th>
              </tr>
            </thead>
            <tbody>
              {interactions.slice(0, 15).map((i) => (
                <tr key={i.id} className="border-b border-base-800 text-base-200">
                  <td className="max-w-xs truncate py-2 pr-4">{i.prompt}</td>
                  <td className="py-2 pr-4 text-base-400">{i.model_used}</td>
                  <td className="py-2 pr-4 text-base-400">{i.latency_ms}ms</td>
                  <td className="py-2">${i.estimated_cost_usd.toFixed(5)}</td>
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
