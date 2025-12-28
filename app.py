import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from utils.extract_text import extract_text
from utils.analyse_resume import analyse_resume
from utils.compare_jobdesc import compare_resume_with_job
from utils.ats_score import calculate_ats_score

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# cuwtom css for button
st.markdown("""
<style>
.big-button button {
    background-color: #4CAF50;
    color: white;
    font-size: 20px;
    padding: 10px 24px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("Resume Analyzer")
st.caption("Analyze your resume against a job description and improve your ATS score")

st.divider()

col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader(
        "Upload Resume (PDF / DOCX)",
        type=["pdf", "docx"]
    )

with col2:
    job_description = st.text_area(
        "Paste Job Description",
        height=220,
        placeholder="Paste job requirements here..."
    )

st.markdown("<div class='big-button'>", unsafe_allow_html=True)
analyze = st.button("Analyze Resume")
st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ANALYSIS ----------------
if analyze:
    if not resume_file or not job_description.strip():
        st.warning("Please upload resume and paste job description.")
    else:
        with st.spinner("Analyzing resume..."):
            resume_text = extract_text(resume_file)

            resume_data = analyse_resume(resume_text)
            resume_skills = resume_data["skills_found"]

            similarity_score, _ = compare_resume_with_job(
                resume_text, job_description
            )

            ats_score = calculate_ats_score(
                resume_skills,
                resume_text,
                job_description
            )

            # skill gap analysis
            job_words = set(job_description.lower().split())
            resume_words = set(resume_text.lower().split())

            missing_skills = list(job_words - resume_words)
            missing_skills = missing_skills[:10]

        st.success(" Analysis Completed")

        m1, m2, m3 = st.columns(3)
        m1.metric("Resume Match", f"{similarity_score:.1f}%")
        m2.metric("ATS Score", f"{ats_score}%")
        m3.metric("Resume Words", resume_data["word_count"])

        st.divider()

        # ats scroe gauge
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=ats_score,
            title={'text': "ATS Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, 40], 'color': "red"},
                    {'range': [40, 70], 'color': "orange"},
                    {'range': [70, 100], 'color': "lightgreen"}
                ],
            }
        ))

        st.plotly_chart(gauge, use_container_width=True)

        # existing skills
        st.subheader("Skills Found in Resume")
        if resume_skills:
            st.write(", ".join(resume_skills))
        else:
            st.warning("No key skills detected.")

        # what skills need to improve
        st.subheader("Skills / Keywords to Improve")

        if missing_skills:
            df = {
                "Skill": missing_skills,
                "Importance": [1] * len(missing_skills)
            }

            fig = px.bar(
                df,
                x="Skill",
                y="Importance",
                color="Skill",
                title="Missing Skills from Job Description"
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success(" Your resume already matches the job well!")
