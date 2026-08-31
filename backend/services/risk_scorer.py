
from config import settings

WEIGHTS = {
    "hallucination_risk": 0.35,  # from rag_checker
    "pii": 0.30,  # from pii_detector
    "safety": 0.35,  # from safety_classifier
}

SAFETY_FLAG_SCORES = {"none": 0, "low": 40, "medium": 70, "high": 100}


def compute_risk_score(hallucination_risk: float, pii_count: int, safety_flag: str) -> dict:
    """Returns {'score': int, 'decision': str, 'breakdown': {...}}."""

    pii_score = min(pii_count * 25, 100)  # each PII hit adds risk, capped at 100
    safety_score = SAFETY_FLAG_SCORES.get(safety_flag, 0)

    weighted = (
        hallucination_risk * WEIGHTS["hallucination_risk"]
        + pii_score * WEIGHTS["pii"]
        + safety_score * WEIGHTS["safety"]
    )
    score = round(min(max(weighted, 0), 100))

    decision = _score_to_decision(score, safety_flag)

    return {
        "score": score,
        "decision": decision,
        "breakdown": {
            "hallucination_risk": hallucination_risk,
            "pii_score": pii_score,
            "safety_score": safety_score,
        },
    }


def _score_to_decision(score: int, safety_flag: str) -> str:
    # A "high" safety flag always forces a block, regardless of the blended score —
    # some risks are non-negotiable.
    if safety_flag == "high":
        return "block"

    if score <= settings.risk_low_max:
        return "allow"
    if score <= settings.risk_medium_max:
        return "verify"
    if score <= settings.risk_high_max:
        return "human_review"
    return "block"
