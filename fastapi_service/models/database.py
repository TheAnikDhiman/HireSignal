"""
HireSignal - Database Schema & SQLAlchemy ORM Models
6-Table PostgreSQL Schema:
1. resumes
2. job_descriptions
3. skills
4. resume_skills (associative junction table with frequency and snippets)
5. scores (fit scoring reports with TF-IDF, skill overlap, vector artifacts)
6. red_flags (ATS rule violations linked to resumes and scores)
"""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    candidate_name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
    file_name = Column(String(255), nullable=True)
    file_type = Column(String(50), nullable=False, default="plain_text")  # pdf, docx, txt
    raw_text = Column(Text, nullable=False)
    cleaned_text = Column(Text, nullable=True)
    total_experience_years = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    resume_skills = relationship("ResumeSkill", back_populates="resume", cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="resume", cascade="all, delete-orphan")
    red_flags = relationship("RedFlag", back_populates="resume", cascade="all, delete-orphan")


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=True, index=True)
    department = Column(String(100), nullable=True)
    seniority_level = Column(String(50), nullable=True)  # Junior, Mid, Senior, Lead, Staff
    raw_text = Column(Text, nullable=False)
    cleaned_text = Column(Text, nullable=True)
    required_experience_years = Column(Float, nullable=True)
    required_skills = Column(JSON, nullable=True)  # list of key skill slugs
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    scores = relationship("Score", back_populates="job_description", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=False, index=True)  # Languages, Frameworks, Cloud, Databases, etc.
    aliases = Column(JSON, nullable=True)  # ["k8s", "kubernetes", "kube"]
    weight = Column(Float, nullable=False, default=1.0)
    is_technical = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    resume_skills = relationship("ResumeSkill", back_populates="skill")


class ResumeSkill(Base):
    __tablename__ = "resume_skills"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(String(36), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False, index=True)
    frequency = Column(Integer, nullable=False, default=1)
    context_snippet = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=False, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    resume = relationship("Resume", back_populates="resume_skills")
    skill = relationship("Skill", back_populates="resume_skills")

    __table_args__ = (
        Index("idx_resume_skill_unique", "resume_id", "skill_id", unique=True),
    )


class Score(Base):
    __tablename__ = "scores"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_description_id = Column(String(36), ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    overall_fit_score = Column(Float, nullable=False)  # 0 to 100
    tfidf_similarity = Column(Float, nullable=False)   # 0.0 to 1.0 (cosine sim)
    skill_overlap_score = Column(Float, nullable=False) # 0.0 to 1.0
    red_flag_penalty = Column(Float, nullable=False, default=0.0)
    matched_skills_count = Column(Integer, nullable=False, default=0)
    missing_skills_count = Column(Integer, nullable=False, default=0)
    matched_skills = Column(JSON, nullable=True)  # List of skill names/slugs
    missing_skills = Column(JSON, nullable=True)  # List of missing skill names
    skill_vector = Column(JSON, nullable=True)    # Structured category vector
    predicted_labels = Column(JSON, nullable=True) # Multi-label classifier output with confidences
    latency_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    resume = relationship("Resume", back_populates="scores")
    job_description = relationship("JobDescription", back_populates="scores")
    red_flags = relationship("RedFlag", back_populates="score", cascade="all, delete-orphan")


class RedFlag(Base):
    __tablename__ = "red_flags"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    score_id = Column(String(36), ForeignKey("scores.id", ondelete="CASCADE"), nullable=True, index=True)
    category = Column(String(100), nullable=False, index=True)
    severity = Column(String(20), nullable=False)  # CRITICAL, WARNING, INFO
    flag_message = Column(String(255), nullable=False)
    context_snippet = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=False)
    penalty_points = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    resume = relationship("Resume", back_populates="red_flags")
    score = relationship("Score", back_populates="red_flags")
