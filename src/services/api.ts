import { FitScoreReport } from '../types';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

interface ApiMatchedSkill {
  name: string;
  slug: string;
  category: string;
  weight: number;
  frequency: number;
  matched_in_jd: boolean;
}

interface ApiRedFlag {
  category: string;
  severity: 'CRITICAL' | 'WARNING' | 'INFO' | 'CLEAN';
  title: string;
  message: string;
  snippet?: string;
  recommendation: string;
  penalty: number;
}

interface ApiClassifierPrediction {
  label: string;
  probability: number;
  is_positive: boolean;
  description: string;
}

interface ApiScoreResponse {
  candidate_name: string;
  role_title: string;
  overall_fit_score: number;
  fit_tier: string;
  score_breakdown: {
    tfidf_similarity: number;
    tfidf_score_scaled: number;
    skill_overlap_score: number;
    skill_score_scaled: number;
    red_flag_penalty_total: number;
    final_weighted_score: number;
    fit_tier: string;
  };
  matched_skills: ApiMatchedSkill[];
  missing_skills: string[];
  resume_skills_total: number;
  jd_skills_total: number;
  skill_signals_vector: Record<string, number>;
  red_flags: ApiRedFlag[];
  classifier_predictions: ApiClassifierPrediction[];
  latency_ms: number;
  timestamp: string;
}

export class HireSignalApiError extends Error {
  status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.name = 'HireSignalApiError';
    this.status = status;
  }
}

async function parseError(response: Response): Promise<string> {
  try {
    const body = await response.json();
    if (typeof body?.detail === 'string') return body.detail;
    if (Array.isArray(body?.detail)) {
      return body.detail.map((item: { msg?: string }) => item.msg || 'Invalid request').join(', ');
    }
  } catch {
    // Fall through to the generic HTTP message.
  }
  return `HireSignal API returned ${response.status} ${response.statusText}`;
}

async function request<T>(path: string, init: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      headers: {
        Accept: 'application/json',
        ...(init.headers || {}),
      },
    });
  } catch {
    throw new HireSignalApiError(
      `Could not reach HireSignal API at ${API_BASE_URL}. Make sure FastAPI is running on port 8000.`
    );
  }

  if (!response.ok) {
    throw new HireSignalApiError(await parseError(response), response.status);
  }

  return response.json() as Promise<T>;
}

function humanizeLabel(label: string): string {
  return label
    .toLowerCase()
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

function normalizeFitTier(tier: string): FitScoreReport['fitTier'] {
  if (tier === 'Strong Fit') return 'Strong Fit';
  if (tier === 'Good Fit') return 'Good Fit';
  if (tier === 'Moderate Fit') return 'Moderate Fit';
  return 'Low Fit';
}

function normalizeResponse(data: ApiScoreResponse, companyName: string): FitScoreReport {
  return {
    candidateName: data.candidate_name,
    roleTitle: data.role_title,
    companyName,
    overallScore: data.overall_fit_score,
    fitTier: normalizeFitTier(data.fit_tier),
    subscores: {
      tfidfCosine: data.score_breakdown.tfidf_similarity,
      tfidfScoreScaled: data.score_breakdown.tfidf_score_scaled,
      skillOverlapRatio: data.score_breakdown.skill_overlap_score,
      skillScoreScaled: data.score_breakdown.skill_score_scaled,
      redFlagPenalties: data.score_breakdown.red_flag_penalty_total,
    },
    matchedSkills: data.matched_skills.map(skill => ({
      name: skill.name,
      slug: skill.slug,
      category: skill.category,
      weight: skill.weight,
      frequency: skill.frequency,
      matchedInJd: skill.matched_in_jd,
    })),
    missingSkills: data.missing_skills,
    resumeSkillsTotal: data.resume_skills_total,
    jdSkillsTotal: data.jd_skills_total,
    skillVectorByCategory: data.skill_signals_vector,
    redFlags: data.red_flags,
    classifierPredictions: data.classifier_predictions.map(prediction => ({
      label: prediction.label,
      labelTitle: humanizeLabel(prediction.label),
      probability: prediction.probability,
      isPositive: prediction.is_positive,
      description: prediction.description,
    })),
    latencyMs: data.latency_ms,
    timestamp: data.timestamp,
  };
}

export async function scoreResumeAndJob(params: {
  resumeText: string;
  jobDescriptionText: string;
  candidateName: string;
  roleTitle: string;
  companyName: string;
}): Promise<FitScoreReport> {
  const data = await request<ApiScoreResponse>('/score', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      resume_text: params.resumeText,
      job_description_text: params.jobDescriptionText,
      candidate_name: params.candidateName,
      role_title: params.roleTitle,
      file_type: 'plain_text',
    }),
  });

  return normalizeResponse(data, params.companyName);
}

export async function scoreUploadedResume(params: {
  resumeFile: File;
  jobDescriptionText: string;
  candidateName: string;
  roleTitle: string;
  companyName: string;
}): Promise<FitScoreReport> {
  const formData = new FormData();
  formData.append('resume_file', params.resumeFile);
  formData.append('job_description_text', params.jobDescriptionText);
  formData.append('candidate_name', params.candidateName);
  formData.append('role_title', params.roleTitle);

  const data = await request<ApiScoreResponse>('/score-upload', {
    method: 'POST',
    body: formData,
  });

  return normalizeResponse(data, params.companyName);
}

export { API_BASE_URL };
