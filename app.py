import streamlit as st
from src.pdf_parser import extract_text_from_pdf
from src.ats_score import calculate_ats_score
from src.gemini_helper import analyze_resume

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

# Resume Processing
if resume_file:

    st.success(f"Resume Uploaded: {resume_file.name}")

    # Extract Text
    resume_text = extract_text_from_pdf(resume_file)

    # ATS Score
    score, skills_found = calculate_ats_score(resume_text)
    with st.spinner("Analyzing Resume with Gemini AI..."):
        ai_analysis = analyze_resume(resume_text)

    # Resume Preview
    st.subheader("📄 Resume Text Preview")

    st.text_area(
        "Extracted Text",
        resume_text,
        height=300
    )

    # Skills
    st.subheader("🛠 Detected Skills")

    for skill in skills_found:
        st.success(skill)
    st.divider()

    st.subheader("🤖 AI Resume Analysis")

    st.markdown(ai_analysis)

# JD Upload
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
    st.metric("JD Match", "--")

with col3:
    if resume_file:
        st.metric("Skills Found", len(skills_found))
    else:
        st.metric("Skills Found", "--")