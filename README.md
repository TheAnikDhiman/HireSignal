# HireSignal — AI Job-Fit Scorer

HireSignal is an explainable ML-based resume screening system that evaluates how well a resume fits a job description. It combines TF-IDF similarity, curated skill signals, ATS-style red-flag rules, and a multi-label classifier into a structured fit report.

## What it does

- Parses resume PDF, DOCX, and TXT files through FastAPI.
- Extracts 300+ technical skill signals from a curated taxonomy.
- Calculates TF-IDF cosine similarity between the resume and job description.
- Scores skill overlap and combines it with the lexical score.
- Detects ATS-style red flags across 11 rule categories.
- Runs a One-vs-Rest logistic-regression classifier for fit labels.
- Exposes rate-limited FastAPI endpoints.
- Includes a PostgreSQL schema, SQLAlchemy models, Alembic migration, and model artifact.
- Provides a multi-screen React UI for analysis, system architecture, and benchmarks.

## Architecture

```text
React + Vite
    │
    │ JSON / multipart
    ▼
FastAPI
    ├── Text extraction (PDF / DOCX / TXT)
    ├── Skill taxonomy matching
    ├── TF-IDF cosine similarity
    ├── ATS red-flag detector
    ├── Multi-label classifier
    └── PostgreSQL / SQLAlchemy / Alembic
```

The core scoring pipeline is local. **No Gemini/OpenAI API key is required.**

## Project structure

```text
HireSignal/
├── src/                         # React frontend
│   ├── components/
│   ├── data/
│   ├── services/api.ts          # FastAPI client
│   └── types.ts
├── fastapi_service/             # Python ML/API service
│   ├── models/
│   ├── services/
│   ├── ml/
│   ├── alembic/
│   ├── sql/
│   └── main.py
├── .env.example
├── package.json
└── README.md
```

## Prerequisites

- Node.js 18+
- Python 3.11+
- Docker Desktop (recommended for PostgreSQL)

## 1. Start the frontend

From the project root:

```bash
npm install
npm run lint
npm run dev
```

Frontend: `http://localhost:3000`

No `.env` file is required for local development. The frontend defaults to `http://localhost:8000`. To override it, copy `.env.example` to `.env` and set `VITE_API_BASE_URL`.

## 2. Start the FastAPI backend

```powershell
cd fastapi_service
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start PostgreSQL and the API with Docker Compose:

```powershell
docker compose up --build
```

FastAPI:
- `http://localhost:8000`
- `http://localhost:8000/docs`
- `http://localhost:8000/health`

## 3. Run the complete app

Keep both processes running:

```text
Terminal 1: npm run dev
Terminal 2: docker compose up --build
```

Then open `http://localhost:3000`.

## API

### Score text

`POST /score` accepts JSON with `resume_text` and `job_description_text`.

### Score an uploaded resume

`POST /score-upload` accepts multipart form data:

- `resume_file`: PDF, DOCX, or TXT
- `job_description_text`: job description text
- `candidate_name`: candidate name
- `role_title`: target role

The React scorer uses `/score-upload` for real uploaded files, so PDF/DOCX parsing happens in Python rather than in the browser.

## Model benchmark artifact

The included classifier artifact reports:

- Dataset size: 500
- Train samples: 400
- Test samples: 100
- Macro precision: 91.59%
- Micro precision: 88.33%
- Macro recall: 43.39%
- Macro F1: 54.59%

These are the current artifact's evaluation results, not production performance guarantees.

## Security / configuration notes

- Do not commit `.env` or secrets.
- The frontend contains no provider API key.
- CORS is intentionally permissive for local/demo use; tighten `allow_origins` before production deployment.
- Add authentication, persistent rate-limit storage, upload-size enforcement, and stronger isolation before exposing the API publicly.

## Resume-project scope

HireSignal is designed as a portfolio project demonstrating full-stack ML engineering: NLP preprocessing, feature engineering, explainable scoring, classifier evaluation, API design, database modeling, file parsing, and a polished product UI.
