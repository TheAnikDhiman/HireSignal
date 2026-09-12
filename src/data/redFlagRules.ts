export interface RedFlagRuleDef {
  id: string;
  name: string;
  category: string;
  severity: 'CRITICAL' | 'WARNING' | 'INFO';
  description: string;
  atsImpact: string;
  recommendation: string;
}

export const RED_FLAG_RULES: RedFlagRuleDef[] = [
  {
    id: 'MISSING_CONTACT_INFO',
    name: 'Missing Contact Information',
    category: 'Header Integrity',
    severity: 'CRITICAL',
    description: 'Verifies email address, telephone number, and portfolio links in the top header.',
    atsImpact: 'Applicant tracking systems (Workday, Taleo, Greenhouse) auto-reject candidates when contact data cannot be parsed into candidate profiles.',
    recommendation: 'Place your clean email, phone number, and location at the very top of page 1 in plain text.'
  },
  {
    id: 'ATS_FORMATTING_CHOKING',
    name: 'ATS Formatting Choking Hazards',
    category: 'Parsing Safety',
    severity: 'CRITICAL',
    description: 'Detects multi-column tables, text boxes, and graphical delimiters that break linear parsing.',
    atsImpact: 'Older parsers read tables left-to-right across columns, jumbling unrelated job entries and skill listings into unreadable garbage text.',
    recommendation: 'Use a standard single-column layout without embedded tables, icons, or text boxes.'
  },
  {
    id: 'RESUME_LENGTH_DENSITY',
    name: 'Resume Length & Density',
    category: 'Format & Length',
    severity: 'CRITICAL',
    description: 'Checks word count thresholds (< 220 words is incomplete; > 1600 words exceeds human review limits).',
    atsImpact: 'Too brief signals lack of qualifications. Excessively verbose documents cause recruiters to miss key qualifications in 7-second scans.',
    recommendation: 'Target 450 – 850 words for 1 page (0-5 years experience) or 900 – 1400 words for 2 pages (5+ years).'
  },
  {
    id: 'KEYWORD_STUFFING',
    name: 'Keyword Stuffing Heuristic',
    category: 'Content Quality',
    severity: 'WARNING',
    description: 'Flags individual skill or buzzword repetition exceeding 3.5% of total resume word count.',
    atsImpact: 'Modern semantic parsers penalize repetitive keyword dumps and flag them as spam or automated generation.',
    recommendation: 'Contextualize tools inside project sentences rather than repeating standalone skill names.'
  },
  {
    id: 'GENERIC_OBJECTIVE_STATEMENT',
    name: 'Generic Objective Statement',
    category: 'Summary Quality',
    severity: 'WARNING',
    description: 'Detects outdated "seeking a challenging position" clichés in place of an executive summary.',
    atsImpact: 'Demonstrates outdated resume styling and wastes the top 15% visual prime real estate.',
    recommendation: 'Replace with an "Executive Summary" detailing years of experience, core stack, and business impact.'
  },
  {
    id: 'VAGUE_BULLETS_NO_METRICS',
    name: 'Vague Bullets Without Metrics',
    category: 'Impact Scoring',
    severity: 'WARNING',
    description: 'Checks what percentage of bullets contain quantifiable metrics (%, $, scale numbers, latency drops).',
    atsImpact: 'Recruiters and hiring managers rank metric-driven resumes in the 90th percentile of candidate evaluations.',
    recommendation: 'Use the Google X-Y-Z formula: "Accomplished [X] as measured by [Y] by doing [Z]".'
  },
  {
    id: 'INCONSISTENT_DATES',
    name: 'Inconsistent Date Chronology',
    category: 'Timeline Integrity',
    severity: 'WARNING',
    description: 'Flags backwards chronological jumps or missing year ranges between roles.',
    atsImpact: 'Confuses automated experience calculators and creates doubts regarding candidate employment verification.',
    recommendation: 'Maintain strict reverse-chronological order: Most recent job first, followed by previous positions.'
  },
  {
    id: 'OVERINFLATED_SKILL_LISTING',
    name: 'Overinflated Skill Dumping',
    category: 'Content Quality',
    severity: 'WARNING',
    description: 'Flags long comma-separated lists (> 25 tools) without accompanying project evidence.',
    atsImpact: 'Technical interviewers discount laundry lists that have no corresponding bullet points in experience.',
    recommendation: 'Highlight 8-12 core technologies where you have hands-on production depth.'
  },
  {
    id: 'EMPLOYMENT_GAPS',
    name: 'Unannotated Employment Gaps',
    category: 'Career Continuity',
    severity: 'INFO',
    description: 'Detects unexplained date gaps exceeding 24 months in employment history.',
    atsImpact: 'Recruiters frequently ask about unexplained gaps during initial phone screens.',
    recommendation: 'Include brief notes such as "Independent Consulting", "Parental Leave", or "Full-Time Upskilling".'
  },
  {
    id: 'FIRST_PERSON_PRONOUNS',
    name: 'First-Person Pronouns ("I", "my", "me")',
    category: 'Tone & Style',
    severity: 'INFO',
    description: 'Detects frequent use of first-person pronouns instead of implied active verbs.',
    atsImpact: 'Violates standard professional resume writing convention.',
    recommendation: 'Omit "I" and start with past-tense action verbs: "Architected", "Engineered", "Spearheaded".'
  },
  {
    id: 'SHORT_JOB_TENURES',
    name: 'Frequent Short Stints (< 6 Months)',
    category: 'Career Continuity',
    severity: 'INFO',
    description: 'Flags multiple successive tenures under 6 months without contract labels.',
    atsImpact: 'Raises retention concerns unless explicitly labeled as contract or project engagements.',
    recommendation: 'Add labels like "(Contract, 6 months)" or "(Fixed-Term Project)" to short engagements.'
  }
];
