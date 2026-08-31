"""
Database tables.

Interaction: one row per prompt/response pair that passed through ControlPlane.
AuditLog: an append-only trail of every decision made, for compliance and debugging.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    model_used = Column(String, nullable=False)

    # Performance
    hallucination_risk = Column(Float, default=0.0)
    latency_ms = Column(Integer, default=0)

    # Cost
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    estimated_cost_usd = Column(Float, default=0.0)

    # Responsibility
    pii_detected = Column(Integer, default=0)  
    safety_flag = Column(String, default="none") 

    # Overall outcome
    risk_score = Column(Integer, nullable=False)
    decision = Column(String, nullable=False) 


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=False), primary_key=True, default=_uuid)
    interaction_id = Column(UUID(as_uuid=False), index=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    event = Column(String, nullable=False)  # e.g. "scored", "blocked", "sent_to_human"
    detail = Column(Text, default="")
