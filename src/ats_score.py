def calculate_ats_score(text):
    
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
        "scikit-learn"
    ]

    text = text.lower()

    found_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)

    score = int((len(found_skills) / len(skills)) * 100)

    return score, found_skills