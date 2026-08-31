
import numpy as np

TRUSTED_DOCS = [
    "Employees are entitled to 20 days of paid annual leave per calendar year.",
    "All expense reports over $500 require manager approval before reimbursement.",
    "The standard notice period for resignation is 30 days.",
    "Remote employees must be available during core hours of 10am to 4pm local time.",
    "Company laptops must have full-disk encryption enabled at all times.",
]


def _embed(text: str) -> np.ndarray:
    """
    Extremely simple bag-of-words vector so this works with zero dependencies. Replace with a
    real embedding model for meaningful semantic similarity in production.
    """
    vocab = sorted(set(" ".join(TRUSTED_DOCS + [text]).lower().split()))
    vector = np.zeros(len(vocab))
    words = text.lower().split()
    for word in words:
        if word in vocab:
            vector[vocab.index(word)] += 1
    norm = np.linalg.norm(vector)
    return vector / norm if norm > 0 else vector


def check_against_knowledge_base(response_text: str) -> dict:
    """
    Returns the best-matching trusted doc, a similarity score (0-1), and a hallucination_risk
    score (0-100, higher = more likely unsupported by the knowledge base).
    """
    if not TRUSTED_DOCS:
        return {"best_match": None, "similarity": 0.0, "hallucination_risk": 50.0}

    response_vec = _embed(response_text)
    best_score = 0.0
    best_doc = None

    for doc in TRUSTED_DOCS:
        doc_vec = _embed(doc)
        # Pad vectors to the same length for the dot product (vocab differs per call).
        max_len = max(len(response_vec), len(doc_vec))
        a = np.pad(response_vec, (0, max_len - len(response_vec)))
        b = np.pad(doc_vec, (0, max_len - len(doc_vec)))
        similarity = float(np.dot(a, b))
        if similarity > best_score:
            best_score = similarity
            best_doc = doc

    hallucination_risk = round((1 - best_score) * 100, 1)

    return {
        "best_match": best_doc,
        "similarity": round(best_score, 3),
        "hallucination_risk": hallucination_risk,
    }
