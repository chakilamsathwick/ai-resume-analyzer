import streamlit as st
from src.pdf_parser import extract_text_from_pdf
from src.ats_score import calculate_ats_score
from src.gemini_helper import analyze_resume
from src.jd_matcher import calculate_jd_match
from src.interview_generator import generate_interview_questions
from src.cover_letter_generator import generate_cover_letter
from src.resume_rating import get_resume_rating
from src.charts import skills_pie_chart,score_bar_chart
from src.pdf_report import generate_pdf_report
from src.skill_recommender import recommend_skills

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📄",
    layout="wide"
)
st.markdown("""
<style>

/* Main Background */
.main {
    background-color: #0E1117;
}

/* App Title */
h1 {
    text-align: center;
    color: #4CAF50;
}

/* Section Headers */
h2, h3 {
    color: #00C8FF;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 50px;
    font-weight: bold;
    font-size: 16px;
}

/* File Upload Box */
[data-testid="stFileUploader"] {
    border: 2px dashed #4CAF50;
    border-radius: 12px;
    padding: 10px;
}

/* Expander */
.streamlit-expanderHeader {
    font-size: 18px;
    font-weight: bold;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown("""
# 📄 AI Resume Analyzer Pro

### AI-Powered Resume Screening Platform


Analyze resumes, calculate ATS scores, compare with Job Descriptions,
generate interview questions, and create AI-powered cover letters.
""")


st.divider()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:

    st.title("📄 Resume Analyzer")

    st.markdown("---")

    st.markdown("### Features")

    st.markdown("📊 ATS Analysis")
    st.markdown("🤖 AI Resume Review")
    st.markdown("🎯 JD Match")
    st.markdown("🎤 Interview Questions")
    st.markdown("📄 Cover Letter")

    st.markdown("---")

    st.info(
        "Upload a Resume and Job Description to unlock AI features."
    )

# ---------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Resume")

    resume_file = st.file_uploader(
        "Choose Resume PDF",
        type=["pdf"]
    )

with col2:
    st.subheader("💼 Job Description")

    jd_text = st.text_area(
        "Paste Job Description",
        height=250
    )

# ---------------------------------------------------
# BUTTONS
# ---------------------------------------------------
st.divider()

col_a, col_b, col_c, col_d, col_e = st.columns(5)

with col_a:
    run_ats = st.button("📊 ATS Score")

with col_b:
    run_ai = st.button("🤖 AI Analysis")

with col_c:
    run_jd = st.button("🎯 JD Match")

with col_d:
    run_interview = st.button("🎤 Questions")

with col_e:
    run_cover = st.button("📄 Cover Letter")

# ---------------------------------------------------
# PROCESS RESUME
# ---------------------------------------------------
if resume_file:

    resume_text = extract_text_from_pdf(resume_file)

    st.success(f"Resume Uploaded: {resume_file.name}")

    st.divider()

    # Resume Preview
    with st.expander("📄 Resume Preview", expanded=False):
        st.text_area(
            "Extracted Resume Text",
            resume_text,
            height=300
        )

    # ------------------------------------------------
    # ATS ANALYSIS
    # ------------------------------------------------
    if run_ats:

        score, skills_found = calculate_ats_score(resume_text)
        st.session_state["ats_score"]=score 


        st.subheader("📊 ATS Analysis")

        st.metric(
            label="ATS Score",
            value=f"{score}%"
        )
        st.progress(score / 100)

        rating = get_resume_rating(score)

        st.success(f"Resume Rating: {rating}")

        st.subheader("🛠 Detected Skills")

        if skills_found:
            for skill in skills_found:
                st.success(skill)
        else:
            st.warning("No skills detected.")
        st.session_state["skills"] = skills_found
        st.session_state["ats_score"] = score

    # ------------------------------------------------
    # AI ANALYSIS
    # ------------------------------------------------
    if run_ai:

        with st.spinner("Analyzing Resume..."):

            ai_analysis = analyze_resume(resume_text)

        with st.expander(
            "🤖 AI Resume Analysis",
            expanded=True
        ):
            st.markdown(ai_analysis)
        st.session_state["ai_analysis"] = ai_analysis

    # ------------------------------------------------
    # JD MATCH
    # ------------------------------------------------
    if run_jd:

        if not jd_text:
            st.warning("Please paste a Job Description.")
        else:

            match_score, matched_skills, missing_skills = calculate_jd_match(
                resume_text,
                jd_text
            )

            st.subheader("🎯 JD Match Analysis")

            st.metric(
                label="JD Match Score",
                value=f"{match_score}%"
            )

            st.progress(match_score / 100)

            chart1 = skills_pie_chart(
                matched_skills,
                missing_skills
            )

            st.plotly_chart(
                chart1,
                use_container_width=True
            )

            chart2 = score_bar_chart(
                st.session_state.get("ats_score",0),
                match_score
            )

            st.plotly_chart(
                chart2,
                use_container_width=True
            )

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("✅ Matched Skills")

                if matched_skills:
                    for skill in matched_skills:
                        st.success(skill)
                else:
                    st.warning("No matching skills found.")

            with col2:

                st.subheader("❌ Missing Skills")

                if missing_skills:
                    for skill in missing_skills:
                        st.error(skill)
                else:
                    st.success("No missing skills.")
        st.session_state["jd_score"] = match_score
        with st.spinner("Generating Skill Recommendations..."):
            recommendations = recommend_skills(missing_skills)

        with st.expander("🎯 Skill Gap Recommendations"):
            st.markdown(recommendations)

    # ------------------------------------------------
    # INTERVIEW QUESTIONS
    # ------------------------------------------------
    if run_interview:

        if not jd_text:
            st.warning("Please paste a Job Description.")
        else:

            with st.spinner(
                "Generating Interview Questions..."
            ):

                interview_questions = generate_interview_questions(
                    resume_text,
                    jd_text
                )

            with st.expander(
                "🎤 AI Interview Questions",
                expanded=True
            ):
                st.markdown(interview_questions)

    # ------------------------------------------------
    # COVER LETTER
    # ------------------------------------------------
    if run_cover:

        if not jd_text:
            st.warning("Please paste a Job Description.")
        else:

            with st.spinner(
                "Generating Cover Letter..."
            ):

                cover_letter = generate_cover_letter(
                    resume_text,
                    jd_text
                )

            with st.expander(
                "📄 AI Cover Letter",
                expanded=True
            ):
                st.markdown(cover_letter)

                st.download_button(
                    "📥 Download Cover Letter",
                    cover_letter,
                    file_name="cover_letter.txt",
                    mime="text/plain"
                )
st.divider()

st.subheader("📄 Export Analysis Report")

if st.button("Generate PDF Report"):

    pdf_file = generate_pdf_report(
        st.session_state.get("ats_score", 0),
        st.session_state.get("jd_score", 0),
        st.session_state.get("skills", []),
        st.session_state.get(
            "ai_analysis",
            "No analysis available"
        )
    )

    with open(pdf_file, "rb") as file:

        st.download_button(
            label="📥 Download PDF Report",
            data=file,
            file_name="AI_Resume_Report.pdf",
            mime="application/pdf"
        )

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------
st.divider()

st.subheader("📊 Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("ATS Score", score if 'score' in locals() else "--")

with col2:
    st.metric("JD Match", match_score if 'match_score' in locals() else "--")

with col3:
    st.metric("Skills Found", len(st.session_state.get("skills", [])) if "skills" in st.session_state else "--")

st.divider()

st.markdown("""
<center>

Built with ❤️ using

Python | Streamlit | Gemini AI | Plotly

</center>
""",
unsafe_allow_html=True)