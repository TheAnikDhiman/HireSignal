"""
HireSignal - Red-Flag Detection Service
Rule-based ATS & Recruiter check engine across 11 distinct categories:
1. EMPLOYMENT_GAPS: Career hiatuses > 9 months without sabbatical/contract labels
2. MISSING_CONTACT_INFO: Missing email, phone, or professional profile links
3. KEYWORD_STUFFING: Unnatural repetition of single terms (> 3.5% frequency)
4. INCONSISTENT_DATES: Chronological reversals or ambiguous year-only dates
5. GENERIC_OBJECTIVE_STATEMENT: Clichéd "seeking challenging position" statements
6. ATS_FORMATTING_CHOKING: High risk characters, table borders, multi-column artifacts
7. VAGUE_BULLETS_NO_METRICS: Action bullets lacking numbers, percentages, or $ impact
8. OVERINFLATED_SKILL_LISTING: Skill dumps (>25 tools) without project context
9. SHORT_JOB_TENURES: Multiple short stints (< 8 months) in succession
10. RESUME_LENGTH_DENSITY: Too sparse (< 250 words) or excessively verbose (> 1800 words)
11. FIRST_PERSON_PRONOUNS: Pervasive use of "I", "me", "my" instead of executive action verbs
"""

import re
from typing import List, Dict, Any, Tuple
from collections import Counter


def detect_red_flags(resume_text: str, raw_metadata: Dict[str, Any] = None) -> Tuple[List[Dict[str, Any]], float]:
    """
    Run 11 rule-based checks on the resume text.
    Returns:
    - flags: list of detected issues with severity, message, snippet, and recommendation
    - total_penalty: sum of points to deduct from fit score
    """
    flags: List[Dict[str, Any]] = []
    total_penalty = 0.0

    if not resume_text or len(resume_text.strip()) < 50:
        flags.append({
            "category": "CRITICAL_EMPTY",
            "severity": "CRITICAL",
            "title": "Unreadable or Blank Resume",
            "message": "The resume text could not be extracted or contains insufficient characters for ATS processing.",
            "snippet": None,
            "recommendation": "Ensure your resume is exported as a standard text-layer PDF or DOCX file.",
            "penalty": 30.0
        })
        return flags, 30.0

    text_lower = resume_text.lower()
    words = re.findall(r'\b[a-zA-Z0-9_\-\+\#]{2,}\b', text_lower)
    word_count = len(words)

    # 1. MISSING CONTACT INFO
    has_email = bool(re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', resume_text))
    has_phone = bool(re.search(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', resume_text))
    has_linkedin_github = bool(re.search(r'linkedin\.com|github\.com', text_lower))

    missing_contact = []
    if not has_email:
        missing_contact.append("Email address")
    if not has_phone:
        missing_contact.append("Phone number")

    if missing_contact:
        pen = 8.0 if not has_email else 4.0
        flags.append({
            "category": "MISSING_CONTACT_INFO",
            "severity": "CRITICAL" if not has_email else "WARNING",
            "title": f"Missing Essential Contact Information ({', '.join(missing_contact)})",
            "message": f"Resume lacks verified {', '.join(missing_contact)}. Applicant Tracking Systems often auto-reject profiles with unparseable contact headers.",
            "snippet": resume_text[:120].strip() + "...",
            "recommendation": "Place your standard email, phone number, and city/state in plain text at the very top header.",
            "penalty": pen
        })
        total_penalty += pen

    if not has_linkedin_github:
        flags.append({
            "category": "MISSING_PORTFOLIO",
            "severity": "INFO",
            "title": "Missing Professional Profile Link (LinkedIn / GitHub)",
            "message": "No LinkedIn, GitHub, or personal portfolio URL detected in the header.",
            "snippet": None,
            "recommendation": "Include clean links to your GitHub profile or LinkedIn URL for immediate recruiter validation.",
            "penalty": 1.5
        })
        total_penalty += 1.5

    # 2. GENERIC OBJECTIVE STATEMENT
    generic_obj_match = re.search(
        r'(?:objective|career\s+objective)[\s:]+(?:seeking|looking\s+for|to\s+obtain|to\s+secure)[\s\w\.,]+?(?:challenging|dynamic|growth|organization|opportunity|esteemed)',
        text_lower
    )
    if generic_obj_match:
        snip = resume_text[generic_obj_match.start():generic_obj_match.end() + 60]
        flags.append({
            "category": "GENERIC_OBJECTIVE_STATEMENT",
            "severity": "WARNING",
            "title": "Outdated / Clichéd Career Objective",
            "message": "Resume uses an outdated generic objective statement ('seeking a challenging role...') instead of an impact-driven Executive Summary.",
            "snippet": snip.strip(),
            "recommendation": "Replace the generic objective with a 3-sentence 'Professional Summary' highlighting years of experience, core tech stack, and primary business impact.",
            "penalty": 3.0
        })
        total_penalty += 3.0

    # 3. KEYWORD STUFFING
    word_freq = Counter(words)
    tech_candidates = [
        w for w, count in word_freq.items() 
        if count >= 8 and len(w) >= 4 and (count / word_count) > 0.035
        and w not in {"with", "that", "from", "have", "this", "were", "been", "team", "data"}
    ]
    if tech_candidates:
        top_culprit = tech_candidates[0]
        flags.append({
            "category": "KEYWORD_STUFFING",
            "severity": "WARNING",
            "title": f"Potential Keyword Stuffing Detected ('{top_culprit}')",
            "message": f"The term '{top_culprit}' appears {word_freq[top_culprit]} times ({round((word_freq[top_culprit]/word_count)*100, 1)}% of total words). Over-repetition triggers ATS spam heuristics.",
            "snippet": f"Repeated mentions of '{top_culprit}' across multiple sections.",
            "recommendation": "Vary your terminology. Use context-rich verbs and describe the system architecture rather than repeating single keywords.",
            "penalty": 4.0
        })
        total_penalty += 4.0

    # 4. FIRST PERSON PRONOUNS ("I", "MY", "ME")
    first_person_matches = re.findall(r'\b(?:i|my|me|myself|mine)\b', text_lower)
    if len(first_person_matches) >= 4:
        flags.append({
            "category": "FIRST_PERSON_PRONOUNS",
            "severity": "INFO",
            "title": "Excessive First-Person Pronouns",
            "message": f"Found {len(first_person_matches)} instances of first-person pronouns ('I', 'my', 'me'). Professional resume standards mandate implied third-person action verbs.",
            "snippet": f"Found {len(first_person_matches)} occurrences (e.g., 'I built', 'my team').",
            "recommendation": "Rewrite using strong active past-tense verbs (e.g., 'Architected payment pipeline' instead of 'I architected my company's payment pipeline').",
            "penalty": 2.0
        })
        total_penalty += 2.0

    # 5. VAGUE BULLETS (LACK OF METRICS / NUMBERS)
    bullet_lines = [line.strip() for line in resume_text.split('\n') if re.match(r'^(?:[•\-\*]|(?:\d+\.))\s+', line.strip())]
    if len(bullet_lines) >= 4:
        metric_bullets = [b for b in bullet_lines if re.search(r'\b(?:\d+[%kKmMbB]?|\$\d+|\d+\+|\d+x)\b', b)]
        metric_ratio = len(metric_bullets) / len(bullet_lines)
        if metric_ratio < 0.35:
            flags.append({
                "category": "VAGUE_BULLETS_NO_METRICS",
                "severity": "WARNING",
                "title": "Vague Bullet Points Without Quantifiable Impact",
                "message": f"Only {int(metric_ratio * 100)}% of bullet points contain quantifiable numbers, percentages, latency drops, or dollar metrics.",
                "snippet": bullet_lines[0][:90] + "...",
                "recommendation": "Adopt Google's X-Y-Z formula: 'Accomplished [X] as measured by [Y] by doing [Z]'. Example: 'Reduced query latency by 45% via Redis caching.'",
                "penalty": 4.5
            })
            total_penalty += 4.5

    # 6. INCONSISTENT DATES & FORMATTING
    date_years = [int(y) for y in re.findall(r'\b(?:199\d|20[0-2]\d)\b', resume_text)]
    if len(date_years) >= 4:
        # Check if year sequence has sudden chronological jump backwards
        has_reversal = False
        for i in range(len(date_years) - 1):
            if date_years[i] < date_years[i+1] - 4:
                has_reversal = True
                break
        if has_reversal:
            flags.append({
                "category": "INCONSISTENT_DATES",
                "severity": "WARNING",
                "title": "Potential Non-Chronological Date Flow",
                "message": "Experience timeline appears mixed or out of reverse-chronological order.",
                "snippet": f"Detected years: {', '.join(map(str, date_years[:6]))}",
                "recommendation": "Structure all job entries in strict reverse-chronological order (most recent position at the top).",
                "penalty": 3.0
            })
            total_penalty += 3.0

    # 7. EMPLOYMENT GAPS CHECK
    gap_indicators = re.search(r'(?:career\s+break|sabbatical|gap\s+year|unemployed)', text_lower)
    if not gap_indicators and len(date_years) >= 2:
        # If max gap between consecutive sorted years is > 2 years
        sorted_years = sorted(list(set(date_years)))
        gaps = [sorted_years[i+1] - sorted_years[i] for i in range(len(sorted_years)-1)]
        if any(g >= 3 for g in gaps):
            flags.append({
                "category": "EMPLOYMENT_GAPS",
                "severity": "INFO",
                "title": "Unannotated Career Gap (> 2 Years)",
                "message": "Timeline exhibits an apparent gap exceeding 24 months without explanatory notation.",
                "snippet": f"Year span jump detected in dates: {sorted_years}",
                "recommendation": "Add a brief clarifying label such as 'Independent Consulting', 'Upskilling / Certification', or 'Sabbatical' to preserve continuity.",
                "penalty": 2.5
            })
            total_penalty += 2.5

    # 8. ATS FORMATTING CHOKING
    formatting_issues = []
    if '│' in resume_text or '┌' in resume_text or '┼' in resume_text:
        formatting_issues.append("ASCII tables/boxes")
    if re.search(r'[^\x00-\x7F\u2022\u2013\u2014\u2018\u2019\u201C\u201D]{6,}', resume_text):
        formatting_issues.append("Unencoded graphical glyphs")

    if formatting_issues:
        flags.append({
            "category": "ATS_FORMATTING_CHOKING",
            "severity": "CRITICAL",
            "title": f"ATS-Choking Formatting Artifacts ({', '.join(formatting_issues)})",
            "message": "Complex layout structures (multi-column tables, text boxes, or decorative unicode lines) often scramble text stream parsers in Workday, Greenhouse, and Taleo.",
            "snippet": "Detected ASCII table borders or high-density column delimiters.",
            "recommendation": "Use a single-column layout without embedded table grids, text boxes, or complex graphical dividers.",
            "penalty": 6.0
        })
        total_penalty += 6.0

    # 9. RESUME LENGTH & DENSITY
    if word_count < 220:
        flags.append({
            "category": "RESUME_LENGTH_DENSITY",
            "severity": "CRITICAL",
            "title": "Resume Is Too Brief (< 220 words)",
            "message": f"Word count ({word_count} words) is below minimum threshold. Recruiters and ATS bots will flag this as incomplete.",
            "snippet": f"Total word count: {word_count}",
            "recommendation": "Expand experience sections with specific technical achievements, project responsibilities, and methodologies.",
            "penalty": 8.0
        })
        total_penalty += 8.0
    elif word_count > 1600:
        flags.append({
            "category": "RESUME_LENGTH_DENSITY",
            "severity": "INFO",
            "title": "Resume Exceeds Recommended Length (> 1,600 words)",
            "message": f"Resume is approximately {round(word_count / 400, 1)} pages long ({word_count} words). Recruiter scan time averages 7 seconds.",
            "snippet": f"Total word count: {word_count}",
            "recommendation": "Trim older experience (> 8 years ago) and consolidate bullet points to fit a crisp 1 to 2-page format.",
            "penalty": 2.0
        })
        total_penalty += 2.0

    # 10. OVERINFLATED SKILL DUMPING
    skills_header = re.search(r'(?:skills|technical\s+skills|core\s+competencies)[\s:]+([^\n\r]{150,})', text_lower)
    if skills_header and ',' in skills_header.group(1):
        comma_items = [x.strip() for x in skills_header.group(1).split(',') if x.strip()]
        if len(comma_items) >= 28:
            flags.append({
                "category": "OVERINFLATED_SKILL_LISTING",
                "severity": "WARNING",
                "title": "Exhaustive Skill Laundry List (> 25 comma items)",
                "message": f"Found a block containing {len(comma_items)} consecutive listed technologies. Keyword lists without demonstrated project context trigger candidate scrutiny.",
                "snippet": skills_header.group(1)[:100] + "...",
                "recommendation": "Group skills logically into 'Core Stack', 'Familiar', and 'Tools', and ensure each core skill is backed by a bullet point in your experience section.",
                "penalty": 3.5
            })
            total_penalty += 3.5

    # 11. SHORT JOB TENURES / JOB HOPPING SIGNAL
    stint_mentions = re.findall(r'\b(?:\d+\s+months?|\d\s+mos?)\b', text_lower)
    short_stints = [s for s in stint_mentions if re.search(r'\b[1-6]\s+mo', s)]
    if len(short_stints) >= 3 and not re.search(r'contract|consultant|freelance|intern', text_lower):
        flags.append({
            "category": "SHORT_JOB_TENURES",
            "severity": "INFO",
            "title": "Frequent Short Tenures (< 6 Months)",
            "message": "Multiple short-duration roles detected without clarifying tags like 'Contract' or 'Project-Based'.",
            "snippet": f"Detected stints: {', '.join(short_stints[:3])}",
            "recommendation": "Label contract or temporary engagements explicitly (e.g. 'Senior Frontend Consultant (6-Month Contract)').",
            "penalty": 2.0
        })
        total_penalty += 2.0

    # Cap total penalty to 25 points maximum so a good resume isn't completely zeroed out
    total_penalty = min(28.0, total_penalty)

    return flags, total_penalty
