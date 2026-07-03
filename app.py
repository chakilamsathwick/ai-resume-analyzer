import streamlit as st
from src.pdf_parser import extract_text_from_pdf
from src.ats_score import calculate_ats_score
from src.gemini_helper import analyze_resume
from src.jd_matcher import calculate_jd_match
from src.interview_generator import generate_interview_questions

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📄",
    layout="wide"
)

# Header
st.title("📄 AI Resume Analyzer Pro")
st.markdown(
    "Analyze resumes, calculate ATS score, compare with Job Descriptions, and generate interview questions using Generative AI."
)

st.divider()

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.info("Upload your resume and job description.")

# Main Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Resume")
    resume_file = st.file_uploader(
        "Choose Resume PDF",
        type=["pdf"]
    )

with col2:
    st.subheader("💼 Upload Job Description")
    jd_text = st.text_area(
        "Paste Job Description",
        height=250
    )

st.divider()

# Initialize Variables
score = 0
skills_found = []
match_score = 0
matched_skills = []
missing_skills = []

# Resume Processing
if resume_file:

    st.success(f"Resume Uploaded: {resume_file.name}")

    # Extract Resume Text
    resume_text = extract_text_from_pdf(resume_file)

    # ATS Score
    score, skills_found = calculate_ats_score(resume_text)

    # JD Match
    if jd_text:
        match_score, matched_skills, missing_skills = calculate_jd_match(
            resume_text,
            jd_text
        )

    # Gemini Resume Analysis
    with st.spinner("Analyzing Resume with Gemini AI..."):
        ai_analysis = analyze_resume(resume_text)

    # Interview Questions
    if jd_text:
        with st.spinner("Generating Interview Questions..."):
            interview_questions = generate_interview_questions(
                resume_text,
                jd_text
            )

    # Resume Preview
    st.subheader("📄 Resume Text Preview")

    st.text_area(
        "Extracted Text",
        resume_text,
        height=300
    )

    # Detected Skills
    st.subheader("🛠 Detected Skills")

    for skill in skills_found:
        st.success(skill)

    # AI Analysis
    st.divider()

    st.subheader("🤖 AI Resume Analysis")

    st.markdown(ai_analysis)

    # JD Match Analysis
    if jd_text:

        st.divider()

        st.subheader("🎯 Job Description Match Analysis")

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("✅ Matched Skills")

            if matched_skills:
                for skill in matched_skills:
                    st.success(skill)
            else:
                st.warning("No matching skills found")

        with col_b:
            st.subheader("❌ Missing Skills")

            if missing_skills:
                for skill in missing_skills:
                    st.error(skill)
            else:
                st.success("No missing skills")

        # Interview Questions
        st.divider()

        st.subheader("🎤 AI Interview Questions")

        st.markdown(interview_questions)

# JD Upload Confirmation
if jd_text:
    st.success("Job Description Added")

st.divider()

# Dashboard
st.subheader("📊 Analysis Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    if resume_file:
        st.metric("ATS Score", f"{score}%")
    else:
        st.metric("ATS Score", "--")

with col2:
    if resume_file and jd_text:
        st.metric("JD Match", f"{match_score}%")
    else:
        st.metric("JD Match", "--")

with col3:
    if resume_file:
        st.metric("Skills Found", len(skills_found))
    else:
        st.metric("Skills Found", "--")