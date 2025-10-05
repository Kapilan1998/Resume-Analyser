import streamlit as st
import pandas as pd
import plotly.express as px
from utils.extract_text import extract_text
from utils.analyse_resume import analyse_resume
from utils.compare_jobdesc import compare_resume_with_job
from utils.ats_score import calculate_ats_score

# Streamlit Page Setup
st.set_page_config(page_title="📄 Resume Analyser Dashboard", layout="wide", page_icon="📊")

# Custom CSS for better card visibility
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .title {font-size:32px; color:#2c3e50; text-align:center; font-weight:bold;}
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title'>📊 AI Resume Analyser Dashboard</h1>", unsafe_allow_html=True)
st.write("Upload your resume, analyze keywords, and compare it with a job description.")

# Sidebar
st.sidebar.header("⚙️ Configuration")
uploaded_file = st.sidebar.file_uploader("Upload Resume", type=["pdf", "docx"])
job_description = st.sidebar.text_area("Paste Job Description (optional)")
st.sidebar.info("💡 Tip: Paste a job description to check skill match and similarity score.")

# Main Logic
if uploaded_file:
    with st.spinner("🔍 Extracting text from resume..."):
        resume_text = extract_text(uploaded_file)

    st.subheader("📄 Resume Preview")
    st.text_area("Extracted Resume Text", resume_text[:1500] + "...", height=250)

    with st.spinner("🧠 Analyzing resume content..."):
        analysis = analyse_resume(resume_text)

    # Colored Metrics Cards
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"<div style='background-color:#1abc9c; color:white; padding:20px; border-radius:15px; text-align:center'><h4>Total Words</h4><h3>{analysis['word_count']}</h3></div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='background-color:#3498db; color:white; padding:20px; border-radius:15px; text-align:center'><h4>Skills Found</h4><h3>{len(analysis['skills_found'])}</h3></div>", unsafe_allow_html=True)
    col3.markdown(f"<div style='background-color:#9b59b6; color:white; padding:20px; border-radius:15px; text-align:center'><h4>Entities Extracted</h4><h3>{len(analysis['entities_found'])}</h3></div>", unsafe_allow_html=True)

    # Skills Table
    st.subheader("💼 Skills Identified")
    if analysis["skills_found"]:
        df_skills = pd.DataFrame({"Skills": analysis["skills_found"]})
        st.dataframe(df_skills.style.set_properties(**{'background-color': '#f0f9ff','color': '#0a3d62','border-color': '#ffffff'}))
    else:
        st.warning("No predefined skills found in this resume.")

    # Entities Chart
    if analysis["entities_found"]:
        entity_df = pd.DataFrame(analysis["entities_found"], columns=["Text","Label"])
        entity_count = entity_df['Label'].value_counts().reset_index()
        entity_count.columns = ['Entity','Count']
        entity_chart = px.bar(
            entity_count, x='Entity', y='Count',
            color='Entity', title="Named Entity Distribution",
            color_discrete_sequence=px.colors.sequential.PuBu
        )
        st.plotly_chart(entity_chart, use_container_width=True)

    # Job Comparison
    match_score, common_skills = 0, []
    if job_description.strip():
        match_score, common_skills = compare_resume_with_job(resume_text, job_description)
        st.subheader("🎯 Resume Match Score")
        st.metric(label="Match Percentage", value=f"{match_score:.2f}%")
        st.progress(match_score/100)
        st.success(f"🧩 Common Keywords: {', '.join(common_skills) if common_skills else 'None'}")

    # ATS Score
    ats_score = calculate_ats_score(
        resume_skills=analysis["skills_found"],
        resume_text=resume_text,
        job_description=job_description,
        experience_keywords=["experience","years","projects"],
        education_keywords=["bachelor","master","degree","phd"]
    )
    st.subheader("📝 ATS Score")
    st.metric("ATS Score (%)", f"{ats_score}%")
    st.progress(ats_score/100)

    # Common Skills Chart
    if common_skills:
        chart_df = pd.DataFrame({"Skill": common_skills, "Count":[1]*len(common_skills)})
        skill_chart = px.bar(
            chart_df, x="Skill", y="Count", color="Skill",
            color_discrete_sequence=px.colors.sequential.Blues,
            title="Common Skills Between Resume and Job Description"
        )
        st.plotly_chart(skill_chart, use_container_width=True)

else:
    st.info("⬆️ Upload a resume to start the analysis.")
