"""
HireSignal - Fit Scoring Service
Calculates:
1. TF-IDF vectorization with n-grams (1, 2) and sublinear TF
2. Cosine similarity between resume and job description
3. Skill overlap score (weighted by skill criticality)
4. Final weighted composite fit score (0 - 100) combining text signals, skill signals, and ATS red-flag deductions.
"""

import math
import re
from typing import Dict, Any, Tuple


# In-memory TF-IDF cosine similarity computation that works standalone or with scikit-learn
def compute_tfidf_cosine(resume_text: str, jd_text: str) -> float:
    """
    Computes TF-IDF cosine similarity between resume and JD.
    Uses scikit-learn TfidfVectorizer if available, or native sublinear TF-IDF vectorizer.
    """
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True,
            max_features=5000
        )
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        sim = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        return max(0.0, min(1.0, sim))
    except Exception:
        # Native pure-Python implementation of Sublinear TF-IDF Cosine Similarity
        def tokenize(text: str):
            tokens = re.findall(r'\b[a-zA-Z0-9_\-\+\#]{2,20}\b', text.lower())
            stop_words = {
                "the", "and", "a", "to", "of", "in", "is", "for", "with", "on", "as", "by", "at",
                "an", "be", "this", "which", "or", "from", "that", "are", "we", "you", "our", "will"
            }
            filtered = [t for t in tokens if t not in stop_words]
            # Add bigrams
            bigrams = [f"{filtered[i]}_{filtered[i+1]}" for i in range(len(filtered) - 1)]
            return filtered + bigrams

        r_tokens = tokenize(resume_text)
        j_tokens = tokenize(jd_text)

        if not r_tokens or not j_tokens:
            return 0.0

        # Term counts
        from collections import Counter
        r_counts = Counter(r_tokens)
        j_counts = Counter(j_tokens)

        vocabulary = set(r_counts.keys()) | set(j_counts.keys())
        N = 2

        # Compute TF-IDF vectors
        dot_product = 0.0
        r_norm_sq = 0.0
        j_norm_sq = 0.0

        for term in vocabulary:
            df = (1 if term in r_counts else 0) + (1 if term in j_counts else 0)
            idf = math.log((1 + N) / (1 + df)) + 1.0

            r_tf = 1 + math.log(r_counts[term]) if r_counts[term] > 0 else 0
            j_tf = 1 + math.log(j_counts[term]) if j_counts[term] > 0 else 0

            r_tfidf = r_tf * idf
            j_tfidf = j_tf * idf

            dot_product += r_tfidf * j_tfidf
            r_norm_sq += r_tfidf ** 2
            j_norm_sq += j_tfidf ** 2

        denominator = math.sqrt(r_norm_sq) * math.sqrt(j_norm_sq)
        if denominator == 0:
            return 0.0

        sim = dot_product / denominator
        # Calibration curve to map raw cosine similarity to recruiter intuitive percentage
        calibrated = math.pow(sim, 0.75) * 1.15
        return max(0.0, min(1.0, calibrated))


def calculate_fit_score(
    tfidf_sim: float,
    skill_overlap_ratio: float,
    red_flag_penalties: float
) -> Dict[str, Any]:
    """
    Formulates the final composite score:
    - Text Similarity: 40%
    - Skill Signal Overlap: 60%
    - Red Flag Penalty deduction: subtracted directly from weighted sum.
    """
    # Scale both to 0-100
    tfidf_component = tfidf_sim * 100.0 * 0.40
    skill_component = skill_overlap_ratio * 100.0 * 0.60

    raw_weighted = tfidf_component + skill_component
    final_score = raw_weighted - red_flag_penalties

    # Clamp 0 to 100
    final_score = max(5.0, min(99.0, final_score))
    final_score = round(final_score, 1)

    # Determine fit tier
    if final_score >= 80.0:
        fit_tier = "Strong Fit"
    elif final_score >= 65.0:
        fit_tier = "Good Fit"
    elif final_score >= 50.0:
        fit_tier = "Moderate Fit"
    else:
        fit_tier = "Low Fit"

    return {
        "overall_fit_score": final_score,
        "fit_tier": fit_tier,
        "tfidf_similarity": round(tfidf_sim, 3),
        "tfidf_score_scaled": round(tfidf_component, 1),
        "skill_overlap_score": round(skill_overlap_ratio, 3),
        "skill_score_scaled": round(skill_component, 1),
        "red_flag_penalty_total": round(red_flag_penalties, 1)
    }
