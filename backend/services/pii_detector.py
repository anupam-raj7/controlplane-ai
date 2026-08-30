"""
Detects likely personal information (PII) in text using regex patterns.

This is a lightweight stand-in for Microsoft Presidio, chosen so the project runs instantly
with no model downloads. To upgrade to real Presidio:

    pip install presidio-analyzer presidio-anonymizer
    python -m spacy download en_core_web_lg

    from presidio_analyzer import AnalyzerEngine
    analyzer = AnalyzerEngine()
    results = analyzer.analyze(text=text, language="en")

`detect_pii` below returns the same shape (a list of entity dicts + a count), so swapping the
implementation doesn't require touching risk_scorer.py or main.py.
"""

import re

PATTERNS = {
    "EMAIL": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "PHONE": re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "SSN_LIKE": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "CREDIT_CARD": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "IP_ADDRESS": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
}


def detect_pii(text: str) -> dict:
    """Returns {'entities': [{'type': ..., 'value': ...}], 'count': int}."""
    entities = []
    for entity_type, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            entities.append({"type": entity_type, "value": match.group()})

    return {"entities": entities, "count": len(entities)}
