/**
 * Small typed client for talking to the ControlPlane.ai backend. Every dashboard component
 * imports from here instead of calling fetch() directly, so the API shape lives in one place.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type Decision = "allow" | "verify" | "human_review" | "block";

export interface DashboardSummary {
  total_interactions: number;
  avg_risk_score: number;
  total_cost_usd: number;
  blocked_count: number;
  human_review_count: number;
  decisions_breakdown: Record<string, number>;
  model_usage: Record<string, number>;
}

export interface Interaction {
  id: string;
  created_at: string;
  prompt: string;
  response: string;
  model_used: string;
  risk_score: number;
  decision: Decision;
  estimated_cost_usd: number;
  safety_flag: string;
  pii_detected: number;
  hallucination_risk: number;
  latency_ms: number;
}

export interface EvaluateResult {
  id: string;
  response: string;
  model_used: string;
  risk_score: number;
  decision: Decision;
  breakdown: Record<string, number>;
  latency_ms: number;
  estimated_cost_usd: number;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Request to ${path} failed with status ${res.status}`);
  }
  return res.json();
}

export const api = {
  getSummary: () => request<DashboardSummary>("/api/dashboard/summary"),
  getInteractions: (decision?: string) =>
    request<Interaction[]>(`/api/dashboard/interactions${decision ? `?decision=${decision}` : ""}`),
  evaluate: (prompt: string) =>
    request<EvaluateResult>("/api/evaluate", {
      method: "POST",
      body: JSON.stringify({ prompt }),
    }),
};
