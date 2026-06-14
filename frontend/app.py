import sys
from pathlib import Path

import streamlit as st
from PyPDF2 import PdfReader

# Connect frontend to backend folder
project_folder = Path(__file__).resolve().parent.parent
backend_folder = project_folder / "backend"
sys.path.append(str(backend_folder))

from career_engine import (
    analyze_career_profile,
    analyze_resume_text,
    create_profile_from_resume,
    generate_text_report,
    analyze_job_description,
    compare_resume_to_job,
    generate_course_plan,
    generate_hr_report,
    generate_mode_report
)


skill_display_names = {
    "python_skill": "Python Skill",
    "math_skill": "Mathematics Skill",
    "data_skill": "Data Analysis Skill",
    "ai_skill": "Artificial Intelligence Skill",
    "communication_skill": "Communication Skill"
}


def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


st.set_page_config(
    page_title="TalentBridge AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 TalentBridge AI Career Analyzer")

st.write(
    "This app analyzes your skills, calculates your career readiness score, "
    "finds skill gaps, recommends portfolio projects, and creates a personalized course plan."
)

# -----------------------------
# User Mode
# -----------------------------
user_mode = st.selectbox(
    "Who are you using this app as?",
    [
        "Job Seeker",
        "HR / Recruiter",
        "Training Center"
    ]
)

if user_mode == "Job Seeker":
    st.info(
        "Job Seeker Mode: Upload your resume, compare it with a job description, "
        "find your skill gaps, and get a personalized learning path."
    )
elif user_mode == "HR / Recruiter":
    st.info(
        "HR / Recruiter Mode: Evaluate candidate-job fit, identify strengths and gaps, "
        "and generate an HR candidate report."
    )
else:
    st.info(
        "Training Center Mode: Use skill gaps to create a course plan and student development pathway."
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

uploaded_resume = st.file_uploader(
    "Upload your resume PDF",
    type=["pdf"]
)

pdf_text = ""

if uploaded_resume is not None:
    pdf_text = extract_text_from_pdf(uploaded_resume)
    st.success("PDF resume uploaded and text extracted.")

resume_text = st.text_area(
    "Paste your resume text here or use uploaded PDF text",
    value=pdf_text,
    height=200,
    placeholder="Paste resume text, skills, experience, or project descriptions here..."
)

# -----------------------------
# Job Description Matching
# -----------------------------
st.subheader("Job Description Matching")

job_description_text = st.text_area(
    "Paste the job description here",
    height=200,
    placeholder="Paste the job posting or job requirements here..."
)

if st.button("Compare Resume to Job Description", key="compare_resume_job_button"):
    if resume_text.strip() == "":
        st.warning("Please paste your resume text or upload a resume PDF first.")
    elif job_description_text.strip() == "":
        st.warning("Please paste a job description first.")
    else:
        resume_skills = analyze_resume_text(resume_text)
        job_required_skills = analyze_job_description(job_description_text)
        job_comparison = compare_resume_to_job(resume_skills, job_required_skills)
        hr_report = generate_hr_report(job_comparison)

        mode_report_text = generate_mode_report(
            user_mode,
            job_comparison,
            hr_report
        )

        st.subheader("Job Match Result")

        st.metric(
            label="Job Match Score",
            value=f"{job_comparison['match_score']}%"
        )

        st.write("Resume Skills Detected:")
        st.write(resume_skills)

        st.write("Job Required Skills Detected:")
        st.write(job_required_skills)

        st.write("Matched Skills:")
        if len(job_comparison["matched_skills"]) == 0:
            st.write("No matched skills found.")
        else:
            for skill in job_comparison["matched_skills"]:
                st.success(skill)

        st.write("Missing Skills:")
        if len(job_comparison["missing_skills"]) == 0:
            st.success("No missing skills. Strong match.")
        else:
            for skill in job_comparison["missing_skills"]:
                st.warning(skill)

        # -----------------------------
        # Mode-Based Output
        # -----------------------------
        if user_mode == "Job Seeker":
            st.subheader("Personalized Course Plan")

            if len(job_comparison["missing_skills"]) == 0:
                st.success("You are a strong match. Start preparing for interviews.")
            else:
                course_plan = generate_course_plan(job_comparison["missing_skills"])

                for skill, lessons in course_plan.items():
                    st.markdown(f"### {skill}")
                    for lesson in lessons:
                        st.write(f"- {lesson}")

            st.subheader("Portfolio Evidence Checklist")

            if len(job_comparison["missing_skills"]) == 0:
                st.write("- Add your best 1–2 portfolio projects to your resume.")
                st.write("- Prepare interview stories for your strongest skills.")
            else:
                for skill in job_comparison["missing_skills"]:
                    st.write(f"- Build one small project that proves your {skill} skill.")

        elif user_mode == "HR / Recruiter":
            st.subheader("HR Candidate Report")

            st.write("**Candidate Recommendation:**", hr_report["recommendation"])
            st.write("**HR Decision:**", hr_report["decision"])
            st.write("**Job Match Score:**", f"{hr_report['match_score']}%")

            st.write("**Candidate Strengths:**")
            if len(hr_report["strengths"]) == 0:
                st.write("No major strengths detected.")
            else:
                for skill in hr_report["strengths"]:
                    st.success(skill)

            st.write("**Candidate Skill Gaps:**")
            if len(hr_report["skill_gaps"]) == 0:
                st.success("No major gaps detected.")
            else:
                for skill in hr_report["skill_gaps"]:
                    st.warning(skill)

            st.write("**HR Summary:**")
            st.info(hr_report["summary"])

        else:
            st.subheader("Training Center Learning Pathway")

            if len(job_comparison["missing_skills"]) == 0:
                st.success("This learner is ready for advanced placement or interview preparation.")
            else:
                course_plan = generate_course_plan(job_comparison["missing_skills"])

                st.write("Recommended student learning pathway:")

                week_number = 1

                for skill, lessons in course_plan.items():
                    st.markdown(f"### Week {week_number}: {skill}")
                    for lesson in lessons:
                        st.write(f"- {lesson}")
                    week_number += 1

        st.download_button(
            label="Download Full Mode Report",
            data=mode_report_text,
            file_name="talentbridge_full_mode_report.txt",
            mime="text/plain"
        )

# -----------------------------
# Resume-Based Career Readiness
# -----------------------------
if st.button("Analyze Resume Skills", key="analyze_resume_skills_button"):
    if resume_text.strip() == "":
        st.warning("Please paste resume text first or upload a resume PDF.")
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

if st.button("Analyze My Career Readiness", key="manual_readiness_button"):
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