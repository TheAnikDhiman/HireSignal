# HireSignal — AI Job-Fit Scorer

**HireSignal** is an ML-based system that scores how well a candidate's resume fits a job description, extracts high-dimensional skill signals from a 312+ taxonomy, and flags ATS-style formatting and recruiter red flags.

> *"See the fit, before the interview."*

---

## 1. System Architecture

```
                                 [ Candidate Resume ] (PDF / DOCX / Text)
                                          │
                                          ▼
                                ┌───────────────────┐
                                │  Text Extraction  │
                                │   & Clean Normal  │
                                └─────────┬─────────┘
                                          │
         ┌────────────────────────────────┼────────────────────────────────┐
         ▼                                ▼                                ▼
┌─────────────────┐             ┌──────────────────┐             ┌──────────────────┐
│  TF-IDF Cosine  │             │   Skill Signal   │             │   ATS Red-Flag   │
│ Semantic Sim.   │             │  312+ Taxonomy   │             │  11 Rule Engine  │
│ (Sublinear TF,  │             │ (Regex Boundaries│             │ (Gaps, Stuffing, │
│  N-gram 1-2)    │             │  Weighted Overlap│             │  Format Choke)   │
└────────┬────────┘             └─────────┬────────┘             └─────────┬────────┘
         │                                │                                │
         └────────────────────────────────┼────────────────────────────────┘
                                          ▼
                             ┌─────────────────────────┐
                             │ Composite Fit Scorer    │
                             │ (TF-IDF + Skills - ATS) │
                             └────────────┬────────────┘
                                          │
                                          ▼
                             ┌─────────────────────────┐
                             │ Multi-Label Classifier  │
                             │ (OneVsRest Logistic Reg)│
                             │ Target: 85%+ Precision  │
                             │ Actual: 91.6% Precision │
                             └────────────┬────────────┘
                                          │
                                          ▼
                             ┌─────────────────────────┐
                             │ Fast JSON Scored Report │
                             │  Latency: < 1.4 seconds │
                             └─────────────────────────┘
```

---

## 2. Core Components

### 1. Text Extraction (`services/text_extractor.py`)
- Standardizes Unicode bullets, dashes, non-breaking spaces, and multi-line breaks.
- Supports PDF extraction with `pypdf` and fallback raw byte stream parsers.
- Supports DOCX via `python-docx` and XML namespace tree parser.

### 2. Skill Signal Extraction (`services/skill_extractor.py`)
- Curated **312+ technical and engineering skills** across 8 categories:
  - Languages (Python, Go, TypeScript, Java, Rust, C++, SQL, etc.)
  - Frameworks (FastAPI, React, Next.js, Django, Spring Boot, etc.)
  - Databases (PostgreSQL, Redis, MongoDB, Elasticsearch, Cassandra, etc.)
  - Cloud & Infra (AWS, GCP, Docker, Kubernetes, Terraform, etc.)
  - Architecture (Apache Kafka, Microservices, Event-Driven, gRPC, etc.)
  - AI & ML (PyTorch, Scikit-learn, NLP, LLMs, Vector DBs, TF-IDF, etc.)
  - DevOps & Observability (Datadog, Prometheus, Grafana, OpenTelemetry, etc.)
  - Testing & Security (PyTest, OAuth 2.0, PCI-DSS, TDD, etc.)
- Boundary-safe regexes prevent false positives (e.g. `\bGo\b` without matching "going", `\bC\+\+\b`, `\bJava\b(?!script)`).
- Outputs structured skill vectors and frequency counters.

### 3. Fit Scoring Engine (`services/fit_scorer.py`)
- Computes Sublinear TF-IDF cosine similarity between resume and job description.
- Computes weighted skill-overlap ratio based on critical requirement weights.
- Composite formula:
  $$\text{Raw Weighted Score} = (\text{TF-IDF Sim} \times 40) + (\text{Skill Overlap Ratio} \times 60)$$
  $$\text{Final Score} = \max(5, \min(99, \text{Raw Weighted Score} - \text{Red Flag Penalties}))$$

### 4. Rule-Based Red-Flag Detection (`services/red_flag_detector.py`)
Audits resumes against 11 ATS & recruiter rejection heuristics:
1. `MISSING_CONTACT_INFO`: Missing verified email or phone number.
2. `ATS_FORMATTING_CHOKING`: Multi-column tables, ASCII boxes, or unencoded characters.
3. `KEYWORD_STUFFING`: Unnatural repetition of single terms (> 3.5% frequency).
4. `GENERIC_OBJECTIVE_STATEMENT`: Outdated "seeking challenging role" clichés.
5. `VAGUE_BULLETS_NO_METRICS`: Action bullets lacking numbers, percentages, or $ impact.
6. `INCONSISTENT_DATES`: Reversed chronological order or overlapping timelines.
7. `EMPLOYMENT_GAPS`: Unannotated career hiatuses > 24 months.
8. `OVERINFLATED_SKILL_LISTING`: Listing > 25 tools without demonstrated experience evidence.
9. `SHORT_JOB_TENURES`: High frequency of short (< 6 month) hops.
10. `RESUME_LENGTH_DENSITY`: Resumes < 220 words (too sparse) or > 1600 words (too verbose).
11. `FIRST_PERSON_PRONOUNS`: Excessive "I", "me", "my" instead of active verbs.

### 5. Multi-Label Classifier (`ml/train_classifier.py` & `ml/eval.py`)
- OneVsRest Classifier with L2-regularized Logistic Regression.
- Target: 85%+ Precision.
- **Evaluation Benchmark Results (500 Samples)**:
  - **Macro Precision: 91.6% (Target >= 85.0% PASSED)**
  - **Micro Precision: 88.3%**
  - **Macro Recall: 43.4%**
  - **Macro F1 Score: 54.6%**
- Predicted Labels:
  - `STRONG_HIRE_FIT` (Precision: 83.3%)
  - `TECH_STACK_MATCH` (Precision: 82.6%)
  - `DOMAIN_EXPERIENCE` (Precision: 92.0%)
  - `SENIORITY_ALIGNMENT` (Precision: 100.0%)
  - `INTERVIEW_PRIORITY` (Precision: 100.0%)

---

## 3. Database Schema (PostgreSQL 6-Table Architecture)

See `fastapi_service/models/database.py` and `fastapi_service/sql/init_schema.sql`.

1. **`resumes`**: Candidate bio, contact information, raw text, and metadata.
2. **`job_descriptions`**: Target role title, company, requirements, and required skills JSON.
3. **`skills`**: Curated skill taxonomy with categories, slug, aliases, and weights.
4. **`resume_skills`**: Junction table mapping skills extracted from resumes with frequency and context.
5. **`scores`**: Calculated fit scores, TF-IDF cosine, skill overlap, latency, and classifier vectors.
6. **`red_flags`**: Detected ATS rule violations with line context and actionable fix recommendations.

---

## 4. API Endpoints

| Method | Endpoint | Description | Rate Limit |
|---|---|---|---|
| `POST` | `/score` | JSON payload scoring (resume + JD text) | 30 / min |
| `POST` | `/score-upload` | File upload (PDF/DOCX/TXT) + JD text | 20 / min |
| `GET` | `/skills` | Returns 312+ skill taxonomy | 120 / min |
| `GET` | `/red-flags/rules` | Lists 11 ATS detection rules | 120 / min |
| `GET` | `/metrics` | Model precision, recall, and F1 report | 120 / min |
| `GET` | `/health` | Health and uptime status | Unlimited |

### Sample cURL Request

```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "Priya Sharma",
    "role_title": "Senior Backend Engineer - Payments",
    "resume_text": "Senior Backend Engineer with 6+ years experience in Python, FastAPI, Go, PostgreSQL, Kafka, and Redis...",
    "job_description_text": "We are seeking a Senior Backend Engineer proficient in Python, Go, and PostgreSQL to scale distributed payments..."
  }'
```

### Sample Response (< 150ms)

```json
{
  "candidate_name": "Priya Sharma",
  "role_title": "Senior Backend Engineer - Payments",
  "overall_fit_score": 78.4,
  "fit_tier": "Good Fit",
  "score_breakdown": {
    "tfidf_similarity": 0.682,
    "tfidf_score_scaled": 27.3,
    "skill_overlap_score": 0.880,
    "skill_score_scaled": 52.8,
    "red_flag_penalty_total": 1.7,
    "final_weighted_score": 78.4,
    "fit_tier": "Good Fit"
  },
  "matched_skills": [
    {"name": "Python", "category": "Languages", "weight": 1.2, "frequency": 4, "matched_in_jd": true},
    {"name": "PostgreSQL", "category": "Databases", "weight": 1.2, "frequency": 3, "matched_in_jd": true},
    {"name": "Apache Kafka", "category": "Architecture", "weight": 1.3, "frequency": 2, "matched_in_jd": true},
    {"name": "Docker", "category": "Cloud & Infra", "weight": 1.2, "frequency": 2, "matched_in_jd": true}
  ],
  "missing_skills": [],
  "red_flags": [],
  "classifier_predictions": [
    {"label": "STRONG_HIRE_FIT", "probability": 0.882, "is_positive": true},
    {"label": "TECH_STACK_MATCH", "probability": 0.941, "is_positive": true},
    {"label": "DOMAIN_EXPERIENCE", "probability": 0.895, "is_positive": true},
    {"label": "SENIORITY_ALIGNMENT", "probability": 0.812, "is_positive": true},
    {"label": "INTERVIEW_PRIORITY", "probability": 0.764, "is_positive": true}
  ],
  "latency_ms": 78.4
}
```

---

## 5. Quickstart & Deployment

### Run with Docker Compose
```bash
docker-compose up --build
```
API available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Run Python Service Standalone
```bash
pip install -r requirements.txt
python ml/train_classifier.py
python ml/eval.py
uvicorn main:app --reload --port 8000
```
