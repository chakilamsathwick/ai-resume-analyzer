def calculate_jd_match(resume_text, jd_text):
    
    skills = [
        "python",
        "sql",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "power bi",
        "tableau",
        "excel",
        "data analysis",
        "git",
        "github",
        "numpy",
        "pandas",
        "scikit-learn",
        "docker",
        "aws",
        "fastapi"
    ]

    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    jd_skills = []
    matched_skills = []

    for skill in skills:
        if skill in jd_text:
            jd_skills.append(skill)

            if skill in resume_text:
                matched_skills.append(skill)

    if len(jd_skills) == 0:
        return 0, [], []

    match_score = int((len(matched_skills) / len(jd_skills)) * 100)

    missing_skills = list(set(jd_skills) - set(matched_skills))

    return match_score, matched_skills, missing_skills