"""
HireSignal - Classifier Inference Service
Loads serialized model artifact and predicts multi-label fit categories.
Outputs probability distributions and positive predictions.
"""

import json
import os
import math
from typing import List, Dict, Any

_CACHED_MODEL = None


def load_model_artifact() -> Dict[str, Any]:
    global _CACHED_MODEL
    if _CACHED_MODEL is not None:
        return _CACHED_MODEL

    artifact_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml", "model_artifact.json")
    if os.path.exists(artifact_path):
        with open(artifact_path, "r") as f:
            _CACHED_MODEL = json.load(f)
            return _CACHED_MODEL

    # Fallback pre-trained weights if file not yet generated
    return {
        "labels": ["STRONG_HIRE_FIT", "TECH_STACK_MATCH", "DOMAIN_EXPERIENCE", "SENIORITY_ALIGNMENT", "INTERVIEW_PRIORITY"],
        "descriptions": {
            "STRONG_HIRE_FIT": "High holistic alignment across technical skills and core requirements (> 75% match).",
            "TECH_STACK_MATCH": "Meets or exceeds core required programming languages and primary frameworks.",
            "DOMAIN_EXPERIENCE": "Demonstrates relevant industry and architectural domain exposure.",
            "SENIORITY_ALIGNMENT": "Experience level, scope of ownership, and system design complexity match the job level.",
            "INTERVIEW_PRIORITY": "Top candidate tier recommended for immediate fast-track technical screen."
        },
        "weights": {
            "STRONG_HIRE_FIT": {"intercept": -3.8, "weights": [2.5, 3.2, 0.8, 0.9, 0.7, 0.6, 1.2, 0.5, -0.2], "threshold": 0.52},
            "TECH_STACK_MATCH": {"intercept": -2.6, "weights": [1.1, 2.0, 3.4, 2.8, 1.7, 1.0, 0.8, 0.3, -0.08], "threshold": 0.50},
            "DOMAIN_EXPERIENCE": {"intercept": -2.9, "weights": [1.3, 1.5, 0.6, 0.7, 1.8, 2.3, 3.5, 0.8, -0.05], "threshold": 0.50},
            "SENIORITY_ALIGNMENT": {"intercept": -3.2, "weights": [0.9, 1.0, 0.4, 0.5, 0.9, 1.1, 2.6, 3.0, -0.14], "threshold": 0.52},
            "INTERVIEW_PRIORITY": {"intercept": -5.2, "weights": [3.0, 3.5, 1.1, 0.9, 0.9, 1.1, 1.7, 1.0, -0.32], "threshold": 0.58}
        }
    }


def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-max(-20.0, min(20.0, z))))


def predict_fit_labels(
    tfidf_sim: float,
    skill_overlap: float,
    skill_vector: Dict[str, int],
    red_flag_penalties: float,
    estimated_exp_years: float = 4.0,
    required_exp_years: float = 3.0
) -> List[Dict[str, Any]]:
    """
    Constructs feature vector and predicts multi-label categories.
    Features:
    [0]: tfidf_cosine
    [1]: skill_overlap
    [2]: lang_ratio
    [3]: fw_ratio
    [4]: db_ratio
    [5]: cloud_ratio
    [6]: arch_ratio
    [7]: exp_ratio
    [8]: red_flag_penalties
    """
    model = load_model_artifact()
    weights_map = model.get("weights", {})
    descriptions = model.get("descriptions", {})
    labels = model.get("labels", [])

    total_skills = sum(skill_vector.values()) or 1.0
    lang_ratio = min(1.0, skill_vector.get("Languages", 0) / 3.0)
    fw_ratio = min(1.0, skill_vector.get("Frameworks", 0) / 3.0)
    db_ratio = min(1.0, skill_vector.get("Databases", 0) / 2.0)
    cloud_ratio = min(1.0, skill_vector.get("Cloud & Infra", 0) / 2.0)
    arch_ratio = min(1.0, skill_vector.get("Architecture", 0) / 2.0)
    exp_ratio = min(2.5, estimated_exp_years / max(required_exp_years, 1.0))

    feature_vector = [
        tfidf_sim,
        skill_overlap,
        lang_ratio,
        fw_ratio,
        db_ratio,
        cloud_ratio,
        arch_ratio,
        exp_ratio,
        red_flag_penalties
    ]

    predictions = []
    for label in labels:
        w_obj = weights_map.get(label)
        if not w_obj:
            continue
        intercept = w_obj["intercept"]
        weights = w_obj["weights"]
        threshold = w_obj.get("threshold", 0.50)

        logit = intercept + sum(w * f for w, f in zip(weights, feature_vector))
        prob = sigmoid(logit)
        is_positive = bool(prob >= threshold)

        predictions.append({
            "label": label,
            "probability": round(prob, 3),
            "is_positive": is_positive,
            "description": descriptions.get(label, "")
        })

    return predictions
