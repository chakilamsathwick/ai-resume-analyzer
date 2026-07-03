from src.gemini_helper import model


def generate_cover_letter(resume_text, jd_text):

    prompt = f"""
    Create a professional cover letter based on the following resume and job description.

    Resume:
    {resume_text}

    Job Description:
    {jd_text}

    The cover letter should:
    - Be professional
    - Be concise
    - Highlight relevant skills
    - Explain why the candidate is suitable
    """

    response = model.generate_content(prompt)

    return response.text