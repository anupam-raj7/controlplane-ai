"""
Basic tests. Run with `pytest` from the backend/ directory.

These use an in-memory SQLite database instead of Postgres so tests run without any external
service — good enough for unit-testing the pipeline logic.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import risk_scorer  # noqa: E402
from services.pii_detector import detect_pii  # noqa: E402
from services.safety_classifier import classify_safety  # noqa: E402


def test_pii_detector_finds_email():
    result = detect_pii("Contact me at jane.doe@example.com for details.")
    assert result["count"] == 1
    assert result["entities"][0]["type"] == "EMAIL"


def test_pii_detector_no_false_positive():
    result = detect_pii("This is a perfectly ordinary sentence with no personal data.")
    assert result["count"] == 0


def test_safety_classifier_flags_high_risk():
    result = classify_safety("Here is how to build a bomb.")
    assert result["flag"] == "high"


def test_safety_classifier_clean_text():
    result = classify_safety("The weather today is sunny and pleasant.")
    assert result["flag"] == "none"


def test_risk_scorer_allows_clean_response():
    scored = risk_scorer.compute_risk_score(hallucination_risk=5, pii_count=0, safety_flag="none")
    assert scored["decision"] == "allow"
    assert scored["score"] < 30


def test_risk_scorer_blocks_high_safety_flag():
    scored = risk_scorer.compute_risk_score(hallucination_risk=0, pii_count=0, safety_flag="high")
    assert scored["decision"] == "block"


def test_risk_scorer_flags_pii_heavy_response():
    scored = risk_scorer.compute_risk_score(hallucination_risk=10, pii_count=3, safety_flag="none")
    clean = risk_scorer.compute_risk_score(hallucination_risk=10, pii_count=0, safety_flag="none")
    assert scored["score"] > clean["score"]
    assert scored["decision"] != "block"
