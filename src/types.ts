/**
 * HireSignal - Type Definitions
 */

export interface SkillItem {
  name: string;
  slug: string;
  category: 'Languages' | 'Frameworks' | 'Databases' | 'Cloud & Infra' | 'Architecture' | 'AI & ML' | 'DevOps' | 'Testing & Quality' | 'Security' | 'Methodologies';
  weight: number;
  pattern: string;
  matchedInResume?: boolean;
  matchedInJd?: boolean;
  frequency?: number;
}

export interface MatchedSkillDetail {
  name: string;
  slug: string;
  category: string;
  weight: number;
  frequency: number;
  matchedInJd: boolean;
}

export type RedFlagSeverity = 'CRITICAL' | 'WARNING' | 'INFO' | 'CLEAN';

export interface RedFlagAuditItem {
  category: string;
  title: string;
  severity: RedFlagSeverity;
  message: string;
  snippet?: string;
  recommendation: string;
  penalty: number;
}

export interface ClassifierPredictionResult {
  label: string;
  labelTitle: string;
  probability: number;
  isPositive: boolean;
  description: string;
}

export interface FitScoreReport {
  candidateName: string;
  roleTitle: string;
  companyName: string;
  overallScore: number;
  fitTier: 'Strong Fit' | 'Good Fit' | 'Moderate Fit' | 'Low Fit';
  subscores: {
    tfidfCosine: number;
    tfidfScoreScaled: number;
    skillOverlapRatio: number;
    skillScoreScaled: number;
    redFlagPenalties: number;
  };
  matchedSkills: MatchedSkillDetail[];
  missingSkills: string[];
  resumeSkillsTotal: number;
  jdSkillsTotal: number;
  skillVectorByCategory: Record<string, number>;
  redFlags: RedFlagAuditItem[];
  classifierPredictions: ClassifierPredictionResult[];
  latencyMs: number;
  timestamp: string;
}

export interface PresetResume {
  id: string;
  name: string;
  title: string;
  experienceYears: number;
  fileName: string;
  summary: string;
  text: string;
}

export interface PresetJobDescription {
  id: string;
  title: string;
  company: string;
  seniority: string;
  location: string;
  text: string;
}
