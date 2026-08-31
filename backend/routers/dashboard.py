
from collections import Counter

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
import models
from schemas import DashboardSummary, InteractionOut

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def summary(db: Session = Depends(get_db)):
    interactions = db.query(models.Interaction).all()

    if not interactions:
        return DashboardSummary(
            total_interactions=0,
            avg_risk_score=0.0,
            total_cost_usd=0.0,
            blocked_count=0,
            human_review_count=0,
            decisions_breakdown={},
            model_usage={},
        )

    decisions = Counter(i.decision for i in interactions)
    models_used = Counter(i.model_used for i in interactions)
    avg_score = sum(i.risk_score for i in interactions) / len(interactions)
    total_cost = sum(i.estimated_cost_usd for i in interactions)

    return DashboardSummary(
        total_interactions=len(interactions),
        avg_risk_score=round(avg_score, 1),
        total_cost_usd=round(total_cost, 4),
        blocked_count=decisions.get("block", 0),
        human_review_count=decisions.get("human_review", 0),
        decisions_breakdown=dict(decisions),
        model_usage=dict(models_used),
    )


@router.get("/interactions", response_model=list[InteractionOut])
def list_interactions(
    limit: int = Query(default=50, le=200),
    decision: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Interaction).order_by(models.Interaction.created_at.desc())
    if decision:
        query = query.filter(models.Interaction.decision == decision)
    return query.limit(limit).all()
