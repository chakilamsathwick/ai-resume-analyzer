def get_resume_rating(score):
    
    if score >= 80:
        return "🟢 Strong Candidate"

    elif score >= 60:
        return "🟡 Good Candidate"

    elif score >= 40:
        return "🟠 Average Candidate"

    else:
        return "🔴 Needs Improvement"