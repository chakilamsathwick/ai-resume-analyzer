from src.gemini_helper import model


def generate_interview_questions(resume_text, jd_text):

    prompt = f"""
    Based on the resume and job description below,
    generate:

    1. Five Technical Interview Questions
    2. Five HR Interview Questions
    3. Five Project-Based Interview Questions

    Resume:
    {resume_text}

    Job Description:
    {jd_text}
    """

    response = model.generate_content(prompt)

    return response.text