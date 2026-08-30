"""Pydantic models for request/response validation (kept separate from the DB models above)."""

from datetime import datetime

from pydantic import BaseModel, Field


class EvaluateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="The user's prompt to send through the pipeline")
    force_model: str | None = Field(
        default=None, description="Optional: force a specific model instead of letting the router choose"
    )


class EvaluateResponse(BaseModel):
    id: str
    response: str
    model_used: str
    risk_score: int
    decision: str
    breakdown: dict
    latency_ms: int
    estimated_cost_usd: float


class InteractionOut(BaseModel):
    id: str
    created_at: datetime
    prompt: str
    response: str
    model_used: str
    risk_score: int
    decision: str
    estimated_cost_usd: float
    safety_flag: str
    pii_detected: int
    hallucination_risk: float
    latency_ms: int

    class Config:
        from_attributes = True


class DashboardSummary(BaseModel):
    total_interactions: int
    avg_risk_score: float
    total_cost_usd: float
    blocked_count: int
    human_review_count: int
    decisions_breakdown: dict[str, int]
    model_usage: dict[str, int]
