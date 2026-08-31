
HIGH_RISK_TERMS = ["kill", "bomb", "weapon", "attack", "exploit vulnerability", "hack into"]
MEDIUM_RISK_TERMS = ["hate", "discriminate", "harass", "illegal drug", "self-harm", "sucide", "cheating"]


def classify_safety(text: str) -> dict:
    """Returns {'flag': 'none' | 'low' | 'medium' | 'high', 'matched_terms': [...]}."""
    lowered = text.lower()

    high_matches = [term for term in HIGH_RISK_TERMS if term in lowered]
    if high_matches:
        return {"flag": "high", "matched_terms": high_matches}

    medium_matches = [term for term in MEDIUM_RISK_TERMS if term in lowered]
    if medium_matches:
        return {"flag": "medium", "matched_terms": medium_matches}

    return {"flag": "none", "matched_terms": []}
