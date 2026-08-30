"""
Flags potentially unsafe or policy-violating content.

This is a lightweight keyword-based stand-in so the project runs with no external calls or
model downloads. To upgrade to a real classifier, swap `classify_safety` for a call to a
hosted moderation API (e.g. OpenAI's moderation endpoint) or a HuggingFace model such as
`unitary/toxic-bert` — keep the same return shape so nothing else needs to change.
"""

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
