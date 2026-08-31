
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import models
from schemas import EvaluateRequest, EvaluateResponse
from services import llm_router, pii_detector, rag_checker, risk_scorer, safety_classifier

router = APIRouter(prefix="/api", tags=["evaluate"])


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate(request: EvaluateRequest, db: Session = Depends(get_db)):
    # 1. Route to a model and call it
    model = llm_router.pick_model(request.prompt, request.force_model)
    result = llm_router.call_model(request.prompt, model)

    # 2. Fact-check the response against trusted docs
    fact_check = rag_checker.check_against_knowledge_base(result["text"])

    # 3. Screen for PII and unsafe content
    pii_result = pii_detector.detect_pii(result["text"])
    safety_result = safety_classifier.classify_safety(result["text"])

    # 4. Combine everything into a risk score + decision
    scored = risk_scorer.compute_risk_score(
        hallucination_risk=fact_check["hallucination_risk"],
        pii_count=pii_result["count"],
        safety_flag=safety_result["flag"],
    )

    # If blocked, don't return the underlying response text to the caller.
    response_text = (
        "[Response blocked by ControlPlane: policy violation detected]"
        if scored["decision"] == "block"
        else result["text"]
    )

    # 5. Persist the interaction
    interaction = models.Interaction(
        prompt=request.prompt,
        response=result["text"],
        model_used=model,
        hallucination_risk=fact_check["hallucination_risk"],
        latency_ms=result["latency_ms"],
        input_tokens=result["input_tokens"],
        output_tokens=result["output_tokens"],
        estimated_cost_usd=result["estimated_cost_usd"],
        pii_detected=pii_result["count"],
        safety_flag=safety_result["flag"],
        risk_score=scored["score"],
        decision=scored["decision"],
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    db.add(
        models.AuditLog(
            interaction_id=interaction.id,
            event=f"scored_{scored['decision']}",
            detail=f"risk_score={scored['score']} model={model}",
        )
    )
    db.commit()

    return EvaluateResponse(
        id=interaction.id,
        response=response_text,
        model_used=model,
        risk_score=scored["score"],
        decision=scored["decision"],
        breakdown=scored["breakdown"],
        latency_ms=result["latency_ms"],
        estimated_cost_usd=result["estimated_cost_usd"],
    )
