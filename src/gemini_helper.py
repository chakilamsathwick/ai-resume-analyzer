import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_resume(resume_text):

    prompt = f"""
    Analyze the following resume.

    Give:

    1. Professional Summary
    2. Strengths
    3. Weaknesses
    4. Improvement Suggestions

    Resume:

    {resume_text}
    """

    response = model.generate_content(prompt)

    return response.text