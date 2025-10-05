def calculate_ats_score(resume_skills, resume_text, job_description, experience_keywords=[], education_keywords=[]):
    """
    Simple ATS Score calculation
    """
    # Skills match
    job_skills = set(job_description.lower().split())
    skills_found = set([s.lower() for s in resume_skills])
    skills_match_pct = len(skills_found & job_skills) / max(len(job_skills),1) * 100

    # Keyword match
    resume_words = set(resume_text.lower().split())
    keyword_match_pct = len(resume_words & job_skills) / max(len(job_skills),1) * 100

    # Experience match
    exp_match_pct = 0
    if experience_keywords:
        exp_found = len(resume_words & set([w.lower() for w in experience_keywords]))
        exp_match_pct = exp_found / max(len(experience_keywords),1) * 100

    # Education match
    edu_match_pct = 0
    if education_keywords:
        edu_found = len(resume_words & set([w.lower() for w in education_keywords]))
        edu_match_pct = edu_found / max(len(education_keywords),1) * 100

    ats_score = 0.4*skills_match_pct + 0.3*keyword_match_pct + 0.2*exp_match_pct + 0.1*edu_match_pct
    return round(ats_score,2)
