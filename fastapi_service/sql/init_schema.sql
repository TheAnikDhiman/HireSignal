-- =============================================================================
-- HireSignal - PostgreSQL 6-Table Relational Schema
-- Tables:
-- 1. resumes
-- 2. job_descriptions
-- 3. skills
-- 4. resume_skills (junction table with context and frequency)
-- 5. scores (fit scoring reports with TF-IDF and skill overlap metrics)
-- 6. red_flags (ATS rule violations with snippets and recommendations)
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Resumes Table
CREATE TABLE IF NOT EXISTS resumes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    candidate_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    linkedin_url VARCHAR(255),
    github_url VARCHAR(255),
    file_name VARCHAR(255),
    file_type VARCHAR(50) NOT NULL DEFAULT 'plain_text',
    raw_text TEXT NOT NULL,
    cleaned_text TEXT,
    total_experience_years NUMERIC(4, 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_resumes_candidate_name ON resumes(candidate_name);
CREATE INDEX IF NOT EXISTS idx_resumes_email ON resumes(email);
CREATE INDEX IF NOT EXISTS idx_resumes_created_at ON resumes(created_at DESC);

-- 2. Job Descriptions Table
CREATE TABLE IF NOT EXISTS job_descriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    department VARCHAR(100),
    seniority_level VARCHAR(50),
    raw_text TEXT NOT NULL,
    cleaned_text TEXT,
    required_experience_years NUMERIC(4, 1),
    required_skills JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_job_descriptions_title ON job_descriptions(title);
CREATE INDEX IF NOT EXISTS idx_job_descriptions_company ON job_descriptions(company);

-- 3. Skills Taxonomy Table
CREATE TABLE IF NOT EXISTS skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(100) NOT NULL,
    aliases JSONB,
    weight NUMERIC(3, 2) DEFAULT 1.00 NOT NULL,
    is_technical BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_skills_slug ON skills(slug);
CREATE INDEX IF NOT EXISTS idx_skills_category ON skills(category);

-- 4. Resume Skills Junction Table
CREATE TABLE IF NOT EXISTS resume_skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    resume_id UUID NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    frequency INTEGER DEFAULT 1 NOT NULL,
    context_snippet TEXT,
    confidence_score NUMERIC(4, 3) DEFAULT 1.000 NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT uq_resume_skill UNIQUE (resume_id, skill_id)
);

CREATE INDEX IF NOT EXISTS idx_resume_skills_resume ON resume_skills(resume_id);
CREATE INDEX IF NOT EXISTS idx_resume_skills_skill ON resume_skills(skill_id);

-- 5. Scores (Fit Scoring Reports)
CREATE TABLE IF NOT EXISTS scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    resume_id UUID NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    job_description_id UUID NOT NULL REFERENCES job_descriptions(id) ON DELETE CASCADE,
    overall_fit_score NUMERIC(5, 2) NOT NULL,
    tfidf_similarity NUMERIC(5, 4) NOT NULL,
    skill_overlap_score NUMERIC(5, 4) NOT NULL,
    red_flag_penalty NUMERIC(5, 2) DEFAULT 0.00 NOT NULL,
    matched_skills_count INTEGER DEFAULT 0 NOT NULL,
    missing_skills_count INTEGER DEFAULT 0 NOT NULL,
    matched_skills JSONB,
    missing_skills JSONB,
    skill_vector JSONB,
    predicted_labels JSONB,
    latency_ms NUMERIC(7, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_scores_resume ON scores(resume_id);
CREATE INDEX IF NOT EXISTS idx_scores_jd ON scores(job_description_id);
CREATE INDEX IF NOT EXISTS idx_scores_overall ON scores(overall_fit_score DESC);

-- 6. Red Flags Table
CREATE TABLE IF NOT EXISTS red_flags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    resume_id UUID NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    score_id UUID REFERENCES scores(id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL,
    severity VARCHAR(20) NOT NULL, -- CRITICAL, WARNING, INFO
    flag_message VARCHAR(255) NOT NULL,
    context_snippet TEXT,
    recommendation TEXT NOT NULL,
    penalty_points NUMERIC(4, 2) DEFAULT 0.00 NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_red_flags_resume ON red_flags(resume_id);
CREATE INDEX IF NOT EXISTS idx_red_flags_category ON red_flags(category);
CREATE INDEX IF NOT EXISTS idx_red_flags_severity ON red_flags(severity);

-- Sample Seed Skills Data
INSERT INTO skills (name, slug, category, weight) VALUES
('Python', 'python', 'Languages', 1.20),
('Go', 'go', 'Languages', 1.20),
('TypeScript', 'typescript', 'Languages', 1.20),
('FastAPI', 'fastapi', 'Frameworks', 1.20),
('React', 'react', 'Frameworks', 1.20),
('PostgreSQL', 'postgresql', 'Databases', 1.20),
('Redis', 'redis', 'Databases', 1.20),
('AWS', 'aws', 'Cloud & Infra', 1.20),
('Kubernetes', 'kubernetes', 'Cloud & Infra', 1.30),
('Docker', 'docker', 'Cloud & Infra', 1.20),
('Apache Kafka', 'kafka', 'Architecture', 1.30),
('Microservices', 'microservices', 'Architecture', 1.20),
('Machine Learning', 'machine-learning', 'AI & ML', 1.20),
('TF-IDF', 'tfidf', 'AI & ML', 1.20),
('CI/CD', 'cicd', 'DevOps', 1.10)
ON CONFLICT (slug) DO NOTHING;
