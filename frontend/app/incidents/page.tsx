"use client";

import { useEffect, useState } from "react";
import { api, Interaction } from "@/lib/api";
import RiskGauge from "@/components/RiskGauge";

const FILTERS = [
  { value: "", label: "All" },
  { value: "block", label: "Blocked" },
  { value: "human_review", label: "Human review" },
  { value: "verify", label: "Verify / edit" },
];

export default function IncidentsPage() {
  const [interactions, setInteractions] = useState<Interaction[]>([]);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    api
      .getInteractions(filter || undefined)
      .then(setInteractions)
      .catch(() => setInteractions([]));
  }, [filter]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-medium text-base-200">Incidents</h1>
        <p className="mt-1 text-sm text-base-400">
          Interactions flagged for verification, human review, or blocked outright.
        </p>
      </div>

      <div className="flex gap-2">
        {FILTERS.map((f) => (
          <button
            key={f.value}
            onClick={() => setFilter(f.value)}
            className={`rounded-md px-3 py-1.5 text-sm ${
              filter === f.value
                ? "bg-base-700 text-base-200"
                : "bg-base-900 text-base-400 hover:text-base-200"
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="space-y-4">
        {interactions.map((i) => (
          <div key={i.id} className="rounded-lg border border-base-700 bg-base-900 p-5">
            <div className="mb-3 flex items-center justify-between">
              <span className="text-xs text-base-400">{new Date(i.created_at).toLocaleString()}</span>
              <span className="text-xs text-base-400">
                model: {i.model_used} · PII hits: {i.pii_detected} · safety: {i.safety_flag}
              </span>
            </div>
            <p className="mb-3 text-sm text-base-200">
              <span className="text-base-400">Prompt: </span>
              {i.prompt}
            </p>
            <p className="mb-3 text-sm text-base-200">
              <span className="text-base-400">Response: </span>
              {i.response}
            </p>
            <RiskGauge score={i.risk_score} />
          </div>
        ))}

        {interactions.length === 0 && (
          <div className="rounded-lg border border-base-700 bg-base-900 p-8 text-center text-sm text-base-400">
            No incidents match this filter.
          </div>
        )}
      </div>
    </div>
  );
}
