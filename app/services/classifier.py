import os
import joblib
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "ml")

EMERGENCY_KEYWORDS = [
    "chest pain", "unconscious", "bleeding", "breathing",
    "seizure", "cardiac arrest", "emergency", "fire", "accident"
]

# Load ML assets ONCE into memory at startup
VECTORIZER = joblib.load(os.path.join(MODEL_DIR, "vectorizer.pkl"))
CAT_MODEL = joblib.load(os.path.join(MODEL_DIR, "category_model.pkl"))
PRIO_MODEL = joblib.load(os.path.join(MODEL_DIR, "priority_model.pkl"))
DEPT_MODEL = joblib.load(os.path.join(MODEL_DIR, "department_model.pkl"))

def predict_complaint(text: str):
    text_vectorized = VECTORIZER.transform([text])

    # Predictions from in-memory models
    category = CAT_MODEL.predict(text_vectorized)[0]
    priority = PRIO_MODEL.predict(text_vectorized)[0]
    department = DEPT_MODEL.predict(text_vectorized)[0]

    # Calculate Confidence Score
    probabilities = CAT_MODEL.predict_proba(text_vectorized)[0]
    confidence = float(np.max(probabilities))

    # Check for Safety & Emergency Keywords
    text_lower = text.lower()
    has_emergency_keyword = any(kw in text_lower for kw in EMERGENCY_KEYWORDS)
    requires_human_review = confidence < 0.70 or has_emergency_keyword or priority == "CRITICAL"

    return {
        "category": category,
        "priority": priority,
        "department": department,
        "confidence": round(confidence, 2),
        "requires_human_review": requires_human_review
    }
