import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def recommend_skills(missing_skills):

    prompt = f"""
    Missing Skills:
    {', '.join(missing_skills)}

    For each missing skill:
    1. Explain why it is important.
    2. Suggest a resource or learning path.
    3. Suggest a mini project.

    Keep it concise.
    """

    response = model.generate_content(prompt)

    return response.text