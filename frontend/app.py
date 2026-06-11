import sys
from pathlib import Path

import streamlit as st

# Connect frontend to backend folder
project_folder = Path(__file__).resolve().parent.parent
backend_folder = project_folder / "backend"
sys.path.append(str(backend_folder))

from career_engine import (
    analyze_career_profile,
    analyze_resume_text,
    create_profile_from_resume,
    generate_text_report
)


skill_display_names = {
    "python_skill": "Python Skill",
    "math_skill": "Mathematics Skill",
    "data_skill": "Data Analysis Skill",
    "ai_skill": "Artificial Intelligence Skill",
    "communication_skill": "Communication Skill"
}


st.set_page_config(
    page_title="TalentBridge AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 TalentBridge AI Career Analyzer")

st.write(
    "This app analyzes your skills, calculates your career readiness score, "
    "finds skill gaps, and recommends portfolio projects."
)

# -----------------------------
# Target Career
# -----------------------------
target_career = st.selectbox(
    "Choose Your Target Career",
    [
        "AI Engineer",
        "Data Analyst",
        "Machine Learning Engineer",
        "AI Education Specialist"
    ]
)

# -----------------------------
# Resume Skill Analyzer
# -----------------------------
st.header("Resume Skill Analyzer")

resume_text = st.text_area(
    "Paste your resume text here",
    height=200,
    placeholder="Paste resume text, skills, experience, or project descriptions here..."
)

if st.button("Analyze Resume Skills"):
    if resume_text.strip() == "":
        st.warning("Please paste resume text first.")
    else:
        detected_skills = analyze_resume_text(resume_text)

        st.subheader("Detected Skills")

        if len(detected_skills) == 0:
            st.write("No skills detected yet. Try adding more resume details.")
        else:
            for skill in detected_skills:
                st.write(f"- {skill}")

            estimated_profile = create_profile_from_resume(detected_skills)

            st.subheader("Estimated Skill Profile From Resume")

            for skill, value in estimated_profile.items():
                if skill != "experience_years":
                    clean_skill_name = skill_display_names.get(skill, skill)
                    st.write(f"- **{clean_skill_name}**: {value}/5")

            resume_result = analyze_career_profile(estimated_profile, target_career)

            st.subheader("Resume-Based Career Readiness")
            st.metric("Resume Readiness Score", f"{resume_result['readiness_score']}%")
            st.write("Status:", resume_result["status"])

            st.subheader("Resume-Based Skill Gaps")

            if len(resume_result["skill_gaps"]) == 0:
                st.write("No major skill gaps found from resume.")
            else:
                for skill, gap in resume_result["skill_gaps"].items():
                    clean_skill_name = skill_display_names.get(skill, skill)
                    st.write(f"- **{clean_skill_name}**: improve by {gap} level(s)")

            st.subheader("Resume-Based Recommended Portfolio Projects")

            if len(resume_result["recommended_projects"]) == 0:
                st.write("Build an advanced end-to-end AI portfolio project.")
            else:
                for skill, projects in resume_result["recommended_projects"].items():
                    clean_skill_name = skill_display_names.get(skill, skill)
                    st.markdown(f"### For {clean_skill_name}")
                    for project in projects:
                        st.write(f"- {project}")

            resume_report_text = generate_text_report(
                resume_result,
                skill_display_names
            )

            st.download_button(
                label="Download Resume-Based Career Report",
                data=resume_report_text,
                file_name="talentbridge_resume_report.txt",
                mime="text/plain"
            )

# -----------------------------
# Manual Skill Analyzer
# -----------------------------
st.header("Enter Your Skill Levels")

python_skill = st.slider("Python Skill", 1, 5, 3)
math_skill = st.slider("Mathematics Skill", 1, 5, 3)
data_skill = st.slider("Data Analysis Skill", 1, 5, 3)
ai_skill = st.slider("Artificial Intelligence Skill", 1, 5, 3)
communication_skill = st.slider("Communication Skill", 1, 5, 3)

experience_years = st.number_input(
    "Years of Experience",
    min_value=0,
    max_value=50,
    value=1
)

user_profile = {
    "python_skill": python_skill,
    "math_skill": math_skill,
    "data_skill": data_skill,
    "ai_skill": ai_skill,
    "communication_skill": communication_skill,
    "experience_years": experience_years
}

if st.button("Analyze My Career Readiness"):
    result = analyze_career_profile(user_profile, target_career)

    st.header("Career Analysis Result")

    st.subheader("Target Career")
    st.write(result["target_career"])

    st.subheader("Career Readiness Score")
    st.metric("Readiness Score", f"{result['readiness_score']}%")

    st.subheader("Status")
    st.success(result["status"])

    st.subheader("Skill Gaps")

    if len(result["skill_gaps"]) == 0:
        st.write("No major skill gaps. You are ready to build advanced projects.")
    else:
        for skill, gap in result["skill_gaps"].items():
            clean_skill_name = skill_display_names.get(skill, skill)
            st.write(f"- **{clean_skill_name}**: improve by {gap} level(s)")

    st.subheader("Recommended Portfolio Projects")

    if len(result["recommended_projects"]) == 0:
        st.write("Build an advanced end-to-end AI portfolio project.")
    else:
        for skill, projects in result["recommended_projects"].items():
            clean_skill_name = skill_display_names.get(skill, skill)
            st.markdown(f"### For {clean_skill_name}")
            for project in projects:
                st.write(f"- {project}")

    report_text = generate_text_report(result, skill_display_names)

    st.download_button(
        label="Download Career Report",
        data=report_text,
        file_name="talentbridge_career_report.txt",
        mime="text/plain"
    )