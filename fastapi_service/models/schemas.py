"""
HireSignal - Pydantic Request & Response Schemas
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class ScoreRequest(BaseModel):
    resume_text: str = Field(..., description="Raw text of the candidate resume")
    job_description_text: str = Field(..., description="Raw text of the job description")
    candidate_name: Optional[str] = Field("Anonymous Candidate", description="Candidate name")
    role_title: Optional[str] = Field("Target Role", description="Job title")
    file_type: Optional[str] = Field("plain_text", description="File format: pdf, docx, plain_text")


class MatchedSkill(BaseModel):
    name: str
    slug: str
    category: str
    weight: float
    frequency: int
    matched_in_jd: bool


class RedFlagItem(BaseModel):
    category: str
    severity: str  # CRITICAL, WARNING, INFO
    title: str
    message: str
    snippet: Optional[str] = None
    recommendation: str
    penalty: float


class ClassifierPrediction(BaseModel):
    label: str
    probability: float
    is_positive: bool
    description: str


class ScoreBreakdown(BaseModel):
    tfidf_similarity: float = Field(..., description="Base cosine similarity score (0.0 to 1.0)")
    tfidf_score_scaled: float = Field(..., description="TF-IDF contribution out of 100")
    skill_overlap_score: float = Field(..., description="Skill match ratio (0.0 to 1.0)")
    skill_score_scaled: float = Field(..., description="Skill contribution out of 100")
    red_flag_penalty_total: float = Field(..., description="Total points deducted by ATS red flags")
    final_weighted_score: float = Field(..., description="Composite fit score (0 to 100)")
    fit_tier: str = Field(..., description="Strong Fit (80+), Moderate Fit (60-79), Low Fit (<60)")


class ScoreResponse(BaseModel):
    candidate_name: str
    role_title: str
    overall_fit_score: float
    fit_tier: str
    score_breakdown: ScoreBreakdown
    matched_skills: List[MatchedSkill]
    missing_skills: List[str]
    resume_skills_total: int
    jd_skills_total: int
    skill_signals_vector: Dict[str, int]
    red_flags: List[RedFlagItem]
    classifier_predictions: List[ClassifierPrediction]
    latency_ms: float
    timestamp: str


class SkillTaxonomyItem(BaseModel):
    name: str
    slug: str
    category: str
    aliases: List[str]
    weight: float


class RedFlagRuleMetadata(BaseModel):
    id: str
    name: str
    category: str
    default_severity: str
    description: str
    ats_impact: str
