import sys
from pathlib import Path

import streamlit as st
from PyPDF2 import PdfReader

# Connect frontend to backend folder
project_folder = Path(__file__).resolve().parent.parent
backend_folder = project_folder / "backend"
sys.path.insert(0, str(backend_folder))

from career_engine import (
    analyze_career_profile,
    analyze_resume_text,
    create_profile_from_resume,
    generate_text_report,
    analyze_job_description,
    compare_resume_to_job,
    generate_course_plan,
    generate_hr_report,
    generate_mode_report,
    generate_progress_tracker,
    calculate_improvement_score,
    prioritize_missing_skills,
    calculate_semantic_match_score,
    calculate_proof_based_readiness_score,
    screen_multiple_candidates,
    generate_interview_readiness_report,
    analyze_skill_confidence


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


def initialize_session_state():
    if "match_result" not in st.session_state:
        st.session_state.match_result = None


initialize_session_state()

st.set_page_config(
    page_title="TalentBridge AI",
    page_icon="🤖",
    layout="wide",
)
st.markdown(
    """
    <style>
    .main {
        background-color: #020617;
    }

    .stApp {
        background-color: #020617;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1 {
        color: #f8fafc;
        font-weight: 800;
    }

    h2, h3 {
        color: #f8fafc;
    }

    p, li, label {
        color: #e5e7eb;
    }

    .stMetric {
        background-color: #111827;
        padding: 16px;
        border-radius: 14px;
        border: 1px solid #334155;
        box-shadow: 0px 2px 8px rgba(15, 23, 42, 0.35);
    }

    div[data-testid="stTabs"] button {
        font-weight: 600;
    }

    .product-card {
        background: linear-gradient(135deg, #111827 0%, #1e293b 100%);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0px 4px 14px rgba(15, 23, 42, 0.35);
        margin-bottom: 20px;
        color: #f8fafc;
    }

    .product-card h1,
    .product-card h2,
    .product-card h3,
    .product-card p {
        color: #f8fafc;
    }

    .product-card small {
        color: #cbd5e1;
    }

    .hero-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #2563eb 100%);
        padding: 32px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
    }

    .hero-box h1 {
        color: white;
        font-size: 42px;
        margin-bottom: 10px;
    }

    .hero-box p {
        font-size: 18px;
        color: #dbeafe;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-box">
        <h1>🤖 TalentBridge AI</h1>
        <p>
        An AI-powered career readiness platform that connects job seekers,
        recruiters, and training centers through resume-job matching,
        skill confidence scoring, portfolio evidence, and interview readiness reports.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="product-card">
            <small>For Job Seekers</small>
            <h2>Close Skill Gaps</h2>
            <p>
            Compare your resume to real job descriptions, identify missing skills,
            and follow a personalized learning path to become job-ready.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="product-card">
            <small>For HR Teams</small>
            <h2>Rank Candidate Fit</h2>
            <p>
            Screen multiple resumes, compare candidate readiness, and see which
            skills are strongly proven versus weakly mentioned.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="product-card">
            <small>For Training Centers</small>
            <h2>Build Learning Paths</h2>
            <p>
            Turn missing skills into structured training plans, portfolio projects,
            and measurable readiness improvement.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()
st.markdown(
    """
    <div class="product-card">
        <h2>Platform Feature Highlights</h2>
        <p>
        TalentBridge AI combines resume analysis, job matching, skill confidence,
        portfolio proof, and HR screening into one career readiness system.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown(
        """
        <div class="product-card">
            <h3>Resume-Job Matching</h3>
            <p>Compare resumes against job descriptions and calculate job readiness.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with feature_col2:
    st.markdown(
        """
        <div class="product-card">
            <h3>Skill Confidence Scoring</h3>
            <p>Identify whether skills are strongly proven or only weakly mentioned.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with feature_col3:
    st.markdown(
        """
        <div class="product-card">
            <h3>HR Batch Screening</h3>
            <p>Rank multiple candidates and generate recruiter-ready reports.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.header("TalentBridge Settings")

user_mode = st.sidebar.selectbox(
    "Who are you using this app as?",
    [
        "Job Seeker",
        "HR / Recruiter",
        "Training Center",
    ],
)

target_career = st.sidebar.selectbox(
    "Choose Your Target Career",
    [
        "AI Engineer",
        "Data Analyst",
        "Machine Learning Engineer",
        "AI Education Specialist",
    ],
)

if user_mode == "Job Seeker":
    st.sidebar.info(
        "Job Seeker Mode: Find your skill gaps and get a personalized learning path."
    )
elif user_mode == "HR / Recruiter":
    st.sidebar.info(
        "HR / Recruiter Mode: Evaluate candidate-job fit and generate an HR report."
    )
else:
    st.sidebar.info(
        "Training Center Mode: Turn skill gaps into a student learning pathway."
    )


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📄 Resume & Job Match",
        "📊 Career Readiness",
        "🚀 Product Vision",
        "💼 Business Case",
        "🏢 HR Batch Screening"
    ]
)

# ==================================================
# TAB 1: RESUME & JOB MATCH
# ==================================================
with tab1:
    st.header("Resume & Job Description Matching")

    uploaded_resume = st.file_uploader(
        "Upload your resume PDF",
        type=["pdf"],
    )

    pdf_text = ""

    if uploaded_resume is not None:
        pdf_text = extract_text_from_pdf(uploaded_resume)
        st.success("PDF resume uploaded and text extracted.")

    resume_text = st.text_area(
        "Paste your resume text here or use uploaded PDF text",
        value=pdf_text,
        height=220,
        placeholder="Paste resume text, skills, experience, or project descriptions here...",
    )

    job_description_text = st.text_area(
        "Paste the job description here",
        height=220,
        placeholder="Paste the job posting or job requirements here...",
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
            improvement_score = calculate_improvement_score(job_comparison)
            semantic_match_score = calculate_semantic_match_score(
                resume_text,
                job_description_text,
            )
            mode_report_text = generate_mode_report(
                user_mode,
                job_comparison,
                hr_report,
            )

            st.session_state.match_result = {
                "resume_text": resume_text,
                "job_description_text": job_description_text,
                "resume_skills": resume_skills,
                "job_required_skills": job_required_skills,
                "job_comparison": job_comparison,
                "hr_report": hr_report,
                "improvement_score": improvement_score,
                "semantic_match_score": semantic_match_score,
                "mode_report_text": mode_report_text,
                "user_mode": user_mode,
            }

    match_result = st.session_state.match_result

    if match_result is not None:
        resume_skills = match_result["resume_skills"]
        job_required_skills = match_result["job_required_skills"]
        job_comparison = match_result["job_comparison"]
        hr_report = match_result["hr_report"]
        improvement_score = match_result["improvement_score"]
        semantic_match_score = match_result["semantic_match_score"]
        mode_report_text = match_result["mode_report_text"]

        st.subheader("Job Match Result")

        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.metric(
                label="Job Match Score",
                value=f"{job_comparison['match_score']}%",
            )

        with metric_col2:
            st.metric(
                label="Semantic Match Score",
                value=f"{semantic_match_score}%",
            )

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.write("**Resume Skills Detected:**")
            if len(resume_skills) == 0:
                st.write("No resume skills detected.")
            else:
                    for skill in resume_skills:
                        st.success(skill)

                    st.subheader("Skill Confidence Scoring")

                    skill_confidence_report = analyze_skill_confidence(
                        resume_text,
                        resume_skills
                    )

                    st.table(skill_confidence_report)

        with result_col2:
            st.write("**Job Required Skills Detected:**")
            if len(job_required_skills) == 0:
                st.write("No job skills detected.")
            else:
                for skill in job_required_skills:
                    st.info(skill)

        st.write("**Matched Skills:**")
        if len(job_comparison["matched_skills"]) == 0:
            st.write("No matched skills found.")
        else:
            for skill in job_comparison["matched_skills"]:
                st.success(skill)

        st.write("**Missing Skills:**")
        if len(job_comparison["missing_skills"]) == 0:
            st.success("No missing skills. Strong match.")
        else:
            for skill in job_comparison["missing_skills"]:
                st.warning(skill)

        st.subheader("Skill Gap Priority Level")

        if len(job_comparison["missing_skills"]) == 0:
            st.success("No missing skills to prioritize.")
        else:
            priority_report = prioritize_missing_skills(
                job_comparison["missing_skills"]
            )
            st.table(priority_report)

        st.subheader("Readiness Improvement Score")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric(
                "Current Score",
                f"{improvement_score['current_score']}%",
            )

        with col_b:
            st.metric(
                "After Training",
                f"{improvement_score['estimated_score_after_training']}%",
            )

        with col_c:
            st.metric(
                "Improvement",
                f"+{improvement_score['improvement_potential']}%",
            )

        st.write(
            "**Status Change:**",
            f"{improvement_score['current_status']} → "
            f"{improvement_score['estimated_status_after_training']}",
        )

        st.subheader("Before-and-After Readiness History")

        readiness_history = [
            {
                "Stage": "Before Training",
                "Score": f"{improvement_score['current_score']}%",
                "Status": improvement_score["current_status"],
            },
            {
                "Stage": "After Recommended Training",
                "Score": f"{improvement_score['estimated_score_after_training']}%",
                "Status": improvement_score["estimated_status_after_training"],
            },
        ]

        st.table(readiness_history)

        # -----------------------------
        # Job Seeker Mode
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

                proof_score = calculate_proof_based_readiness_score(
                    job_comparison["match_score"],
                    semantic_match_score,
                    {},
                    {},
                )

                st.subheader("Proof-Based Readiness Score")

                proof_col1, proof_col2, proof_col3 = st.columns(3)

                with proof_col1:
                    st.metric(
                        "Proof-Based Score",
                        f"{proof_score['proof_based_score']}%",
                    )

                with proof_col2:
                    st.metric(
                        "Portfolio Evidence Score",
                        f"{proof_score['portfolio_evidence_score']}%",
                    )

                with proof_col3:
                    st.metric(
                        "Progress Completion Score",
                        f"{proof_score['progress_completion_score']}%",
                    )

                st.success(proof_score["readiness_level"])
            else:
                for skill in job_comparison["missing_skills"]:
                    st.write(f"- Build one small project that proves your {skill} skill.")

                st.subheader("Candidate Progress Tracker")

                progress_tracker = generate_progress_tracker(
                    job_comparison["missing_skills"]
                )
                st.table(progress_tracker)

                st.subheader("Portfolio Evidence Links and Progress Status")

                evidence_links = {}
                progress_statuses = {}

                with st.form("portfolio_evidence_form"):
                    for skill in job_comparison["missing_skills"]:
                        st.markdown(f"### {skill}")

                        evidence_links[skill] = st.text_input(
                            f"Paste portfolio or GitHub link for {skill}",
                            placeholder="Example: https://github.com/username/project",
                            key=f"evidence_link_{skill}",
                        )

                        progress_statuses[skill] = st.selectbox(
                            f"Progress status for {skill}",
                            [
                                "Not Started",
                                "In Progress",
                                "Completed",
                            ],
                            key=f"progress_status_{skill}",
                        )

                    generate_evidence_summary = st.form_submit_button(
                        "Generate Portfolio Evidence Summary"
                    )

                if generate_evidence_summary:
                    st.subheader("Portfolio Evidence Summary")

                    evidence_report = "TalentBridge AI - Portfolio Evidence and Progress Report\n\n"
                    completed_count = 0
                    total_missing_skills = len(job_comparison["missing_skills"])

                    for skill in job_comparison["missing_skills"]:
                        if progress_statuses[skill] == "Completed":
                            completed_count += 1

                    if total_missing_skills > 0:
                        completion_score = round(
                            (completed_count / total_missing_skills) * 100,
                            2,
                        )
                    else:
                        completion_score = 100

                    st.subheader("Progress Completion Score")

                    score_col1, score_col2, score_col3 = st.columns(3)

                    with score_col1:
                        st.metric("Completed Skills", completed_count)

                    with score_col2:
                        st.metric("Total Missing Skills", total_missing_skills)

                    with score_col3:
                        st.metric("Completion Score", f"{completion_score}%")

                    proof_score = calculate_proof_based_readiness_score(
                        job_comparison["match_score"],
                        semantic_match_score,
                        evidence_links,
                        progress_statuses,
                    )

                    st.subheader("Proof-Based Readiness Score")

                    proof_col1, proof_col2, proof_col3 = st.columns(3)

                    with proof_col1:
                        st.metric(
                            "Proof-Based Score",
                            f"{proof_score['proof_based_score']}%",
                        )

                    with proof_col2:
                        st.metric(
                            "Portfolio Evidence Score",
                            f"{proof_score['portfolio_evidence_score']}%",
                        )

                    with proof_col3:
                        st.metric(
                            "Progress Completion Score",
                            f"{proof_score['progress_completion_score']}%",
                        )

                    st.success(proof_score["readiness_level"])

                    evidence_report += f"Completed Skills: {completed_count}\n"
                    evidence_report += f"Total Missing Skills: {total_missing_skills}\n"
                    evidence_report += f"Progress Completion Score: {completion_score}%\n"
                    evidence_report += f"Proof-Based Readiness Score: {proof_score['proof_based_score']}%\n"
                    evidence_report += f"Portfolio Evidence Score: {proof_score['portfolio_evidence_score']}%\n"
                    evidence_report += f"Proof Readiness Level: {proof_score['readiness_level']}\n\n"

                    for skill in job_comparison["missing_skills"]:
                        link = evidence_links[skill]
                        status = progress_statuses[skill]

                        st.write(f"**Missing Skill:** {skill}")
                        st.write(f"**Portfolio Evidence Link:** {link}")
                        st.write(f"**Progress Status:** {status}")
                        st.divider()

                        evidence_report += f"Missing Skill: {skill}\n"
                        evidence_report += f"Portfolio Evidence Link: {link}\n"
                        evidence_report += f"Progress Status: {status}\n\n"

                    st.download_button(
                        label="Download Portfolio Evidence and Progress Report",
                        data=evidence_report,
                        file_name="talentbridge_portfolio_progress_report.txt",
                        mime="text/plain",
                    )

        # -----------------------------
        # HR / Recruiter Mode
        # -----------------------------
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

            st.subheader("Recruiter Feedback Form")

            candidate_name = st.text_input(
                "Candidate Name",
                placeholder="Enter candidate name",
            )

            recruiter_decision = st.selectbox(
                "Recruiter Decision",
                [
                    "Interview Ready",
                    "Train Before Interview",
                    "Not Ready Yet",
                    "Needs More Portfolio Evidence",
                ],
            )

            recruiter_feedback = st.text_area(
                "Recruiter Feedback",
                placeholder="Write feedback for the candidate...",
            )

            recommended_next_step = st.text_area(
                "Recommended Next Step",
                placeholder="Example: Complete ETL project and add GitHub link.",
            )

            if st.button("Generate Recruiter Feedback Summary"):
                st.subheader("Recruiter Feedback Summary")

                st.write("**Candidate:**", candidate_name)
                st.write("**Decision:**", recruiter_decision)
                st.write("**Feedback:**", recruiter_feedback)
                st.write("**Recommended Next Step:**", recommended_next_step)

                recruiter_feedback_report = f"""
TalentBridge AI - Recruiter Feedback Report

Candidate Name:
{candidate_name}

Recruiter Decision:
{recruiter_decision}

Recruiter Feedback:
{recruiter_feedback}

Recommended Next Step:
{recommended_next_step}

Generated by TalentBridge AI
"""

                st.download_button(
                    label="Download Recruiter Feedback Report",
                    data=recruiter_feedback_report,
                    file_name="talentbridge_recruiter_feedback_report.txt",
                    mime="text/plain",
                )

        # -----------------------------
        # Training Center Mode
        # -----------------------------
        else:
            st.subheader("Training Center Learning Pathway")

            if len(job_comparison["missing_skills"]) == 0:
                st.success(
                    "This learner is ready for advanced placement or interview preparation."
                )
            else:
                course_plan = generate_course_plan(job_comparison["missing_skills"])

                st.write("Recommended student learning pathway:")

                week_number = 1

                for skill, lessons in course_plan.items():
                    st.markdown(f"### Week {week_number}: {skill}")
                    for lesson in lessons:
                        st.write(f"- {lesson}")
                    week_number += 1

            st.subheader("Candidate Progress Tracker")

            if len(job_comparison["missing_skills"]) == 0:
                st.success("No missing skills to track.")
            else:
                progress_tracker = generate_progress_tracker(
                    job_comparison["missing_skills"]
                )
                st.table(progress_tracker)

                st.subheader("Portfolio Evidence Links")

                evidence_links = {}

                for skill in job_comparison["missing_skills"]:
                    evidence_links[skill] = st.text_input(
                        f"Paste portfolio or GitHub link for {skill}",
                        placeholder="Example: https://github.com/username/project",
                        key=f"training_evidence_link_{skill}",
                    )

                if st.button("Generate Portfolio Evidence Summary"):
                    st.subheader("Portfolio Evidence Summary")

                    evidence_report = "TalentBridge AI - Portfolio Evidence Report\n\n"

                    for skill, link in evidence_links.items():
                        st.write(f"**{skill}:** {link}")

                        evidence_report += f"Missing Skill: {skill}\n"
                        evidence_report += f"Portfolio Evidence Link: {link}\n\n"

                    st.download_button(
                        label="Download Portfolio Evidence Report",
                        data=evidence_report,
                        file_name="talentbridge_portfolio_evidence_report.txt",
                        mime="text/plain",
                    )

        st.download_button(
            label="Download Full Mode Report",
            data=mode_report_text,
            file_name="talentbridge_full_mode_report.txt",
            mime="text/plain",
        )

    st.divider()

    st.subheader("Resume-Based Career Readiness")

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
                st.metric(
                    "Resume Readiness Score",
                    f"{resume_result['readiness_score']}%",
                )
                st.write("Status:", resume_result["status"])

                st.subheader("Resume-Based Skill Gaps")

                if len(resume_result["skill_gaps"]) == 0:
                    st.write("No major skill gaps found from resume.")
                else:
                    for skill, gap in resume_result["skill_gaps"].items():
                        clean_skill_name = skill_display_names.get(skill, skill)
                        st.write(
                            f"- **{clean_skill_name}**: improve by {gap} level(s)"
                        )

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
                    skill_display_names,
                )

                st.download_button(
                    label="Download Resume-Based Career Report",
                    data=resume_report_text,
                    file_name="talentbridge_resume_report.txt",
                    mime="text/plain",
                )

# ==================================================
# TAB 2: CAREER READINESS
# ==================================================
with tab2:
    st.header("Manual Career Readiness Analyzer")

    st.write(
        "Use this section when you want to manually estimate your skill levels "
        "and calculate readiness for the selected target career."
    )

    python_skill = st.slider("Python Skill", 1, 5, 3)
    math_skill = st.slider("Mathematics Skill", 1, 5, 3)
    data_skill = st.slider("Data Analysis Skill", 1, 5, 3)
    ai_skill = st.slider("Artificial Intelligence Skill", 1, 5, 3)
    communication_skill = st.slider("Communication Skill", 1, 5, 3)

    experience_years = st.number_input(
        "Years of Experience",
        min_value=0,
        max_value=50,
        value=1,
    )

    user_profile = {
        "python_skill": python_skill,
        "math_skill": math_skill,
        "data_skill": data_skill,
        "ai_skill": ai_skill,
        "communication_skill": communication_skill,
        "experience_years": experience_years,
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
            mime="text/plain",
        )

# ==================================================
# TAB 3: PRODUCT VISION
# ==================================================
with tab3:
    st.header("TalentBridge AI Product Vision")

    st.write(
        "TalentBridge AI is designed to become more than a resume scanner. "
        "It is a career readiness and training platform."
    )

    st.subheader("Who It Helps")

    st.write("**Job Seekers**")
    st.write("- Understand if they are ready for a target role.")
    st.write("- Identify missing skills.")
    st.write("- Receive a personalized learning path.")
    st.write("- Build portfolio evidence for weak areas.")
    st.write("- Track progress toward interview readiness.")

    st.write("**HR / Recruiters**")
    st.write("- Compare candidates against job descriptions.")
    st.write("- See strengths and skill gaps.")
    st.write("- Decide whether to interview, train, or reject.")
    st.write("- Generate HR-style candidate reports.")

    st.write("**Training Centers**")
    st.write("- Turn skill gaps into weekly learning pathways.")
    st.write("- Support career changers and students.")
    st.write("- Create course plans based on real job requirements.")
    st.write("- Track student progress with portfolio evidence.")

    st.subheader("Missing Ingredient This App Solves")

    st.write(
        "Most resume tools only tell users what is missing. TalentBridge AI is designed "
        "to create a feedback loop between job seekers, recruiters, and training programs."
    )

    st.write(
        "The system turns missing skills into learning tasks, portfolio evidence, "
        "and progress tracking so candidates can improve and recruiters can see readiness."
    )

    st.subheader("Future Business Model")

    st.write("- Free resume-job match scan.")
    st.write("- Paid detailed report for job seekers.")
    st.write("- HR candidate screening reports.")
    st.write("- Training center dashboard.")
    st.write("- Portfolio evidence tracking.")
    st.write("- Progress tracking and readiness improvement history.")

# ==================================================
# TAB 4: BUSINESS CASE
# ==================================================
with tab4:
    st.header("TalentBridge AI Business Case")

    st.write(
        "TalentBridge AI is an AI-powered career readiness platform that helps "
        "job seekers, recruiters, and training centers close the gap between "
        "job requirements and candidate skills."
    )

    st.subheader("Problem")

    st.write(
        "Many job seekers do not know why they are not getting interviews. "
        "Recruiters see missing skills, but candidates often do not receive "
        "clear feedback or a path to improve. Training centers also need a way "
        "to connect learning programs directly to real job requirements."
    )

    st.subheader("Solution")

    st.write(
        "TalentBridge AI compares a resume with a job description, identifies "
        "matched and missing skills, creates a personalized learning path, "
        "tracks progress, collects portfolio evidence, and generates recruiter-ready reports."
    )

    st.subheader("Target Users")

    st.write("**1. Job Seekers**")
    st.write("- Understand job match score")
    st.write("- Identify missing skills")
    st.write("- Follow a learning pathway")
    st.write("- Add portfolio evidence")
    st.write("- Track readiness improvement")

    st.write("**2. HR / Recruiters**")
    st.write("- Review candidate-job fit")
    st.write("- See strengths and gaps")
    st.write("- Generate feedback reports")
    st.write("- Recommend training before interview")

    st.write("**3. Training Centers**")
    st.write("- Convert skill gaps into learning plans")
    st.write("- Track learner progress")
    st.write("- Help learners become job-ready")
    st.write("- Align training with real job descriptions")

    st.subheader("Core Value Proposition")

    st.info(
        "TalentBridge AI does not only say what skills are missing. "
        "It shows how the candidate can become ready, prove improvement, "
        "and return with portfolio evidence."
    )

    st.subheader("Product Workflow")

    st.write(
        """
        Resume + Job Description  
        ↓  
        Job Match Score  
        ↓  
        Semantic Match Score  
        ↓  
        Missing Skills  
        ↓  
        Skill Gap Priority Level  
        ↓  
        Readiness Improvement Score  
        ↓  
        Before-and-After Readiness History  
        ↓  
        Personalized Learning Path  
        ↓  
        Portfolio Evidence Links  
        ↓  
        Progress Status  
        ↓  
        Completion Score  
        ↓  
        Proof-Based Readiness Score  
        ↓  
        Recruiter Feedback Report  
        ↓  
        Improved Candidate Readiness
        """
    )

    st.subheader("Possible Business Model")

    st.write("- Free basic resume-job match scan")
    st.write("- Paid detailed career readiness report")
    st.write("- Subscription for job seekers")
    st.write("- HR recruiter dashboard")
    st.write("- Training center dashboard")
    st.write("- Portfolio evidence verification")
    st.write("- Career coaching and AI learning pathway recommendations")

    st.subheader("Why This Project Is Strong for Your Portfolio")

    st.write(
        "This project shows Python, Streamlit, resume parsing, job matching, "
        "AI product thinking, HR workflow design, user-centered design, "
        "and business strategy."
    )
# ==================================================

# TAB 5: HR BATCH RESUME SCREENING

# ==================================================

with tab5:
    st.header("HR Batch Resume Screening")

st.write(
    "Use this section to compare one job description against multiple candidate resumes "
    "and rank candidates by readiness."
)

batch_job_description = st.text_area(
    "Paste the job description for batch screening",
    height=200,
    placeholder="Paste the job description here...",
    key="batch_job_description"
)

st.subheader("Candidate Resumes")

candidate_1_name = st.text_input(
    "Candidate 1 Name",
    value="Candidate 1",
    key="candidate_1_name"
)

candidate_1_resume = st.text_area(
    "Candidate 1 Resume",
    height=180,
    placeholder="Paste Candidate 1 resume text here...",
    key="candidate_1_resume"
)

candidate_2_name = st.text_input(
    "Candidate 2 Name",
    value="Candidate 2",
    key="candidate_2_name"
)

candidate_2_resume = st.text_area(
    "Candidate 2 Resume",
    height=180,
    placeholder="Paste Candidate 2 resume text here...",
    key="candidate_2_resume"
)

candidate_3_name = st.text_input(
    "Candidate 3 Name",
    value="Candidate 3",
    key="candidate_3_name"
)

candidate_3_resume = st.text_area(
    "Candidate 3 Resume",
    height=180,
    placeholder="Paste Candidate 3 resume text here...",
    key="candidate_3_resume"
)

if st.button("Run HR Batch Screening"):
    if batch_job_description.strip() == "":
        st.warning("Please paste a job description first.")
    else:
        candidate_resumes = []

        if candidate_1_resume.strip() != "":
            candidate_resumes.append(
                {
                    "candidate_name": candidate_1_name,
                    "resume_text": candidate_1_resume
                }
            )

        if candidate_2_resume.strip() != "":
            candidate_resumes.append(
                {
                    "candidate_name": candidate_2_name,
                    "resume_text": candidate_2_resume
                }
            )

        if candidate_3_resume.strip() != "":
            candidate_resumes.append(
                {
                    "candidate_name": candidate_3_name,
                    "resume_text": candidate_3_resume
                }
            )

        if len(candidate_resumes) == 0:
            st.warning("Please paste at least one candidate resume.")
        else:
            screening_results = screen_multiple_candidates(
                batch_job_description,
                candidate_resumes
            )

            st.subheader("Ranked Candidate Results")

            display_results = []

            for candidate in screening_results:
               display_results.append(
        {
            "Candidate Name": candidate["Candidate Name"],
            "Job Match Score": f"{candidate['Job Match Score']:.2f}",
            "Semantic Match Score": f"{candidate['Semantic Match Score']:.2f}",
            "Final Screening Score": f"{candidate['Final Screening Score']:.2f}",
            "Matched Skills": candidate["Matched Skills"],
            "Missing Skills": candidate["Missing Skills"],
            "Strong Evidence Skills": candidate["Strong Evidence Skills"],
            "Weak Evidence Skills": candidate["Weak Evidence Skills"],
            "Recommendation": candidate["Recommendation"]
        }
    )

            st.table(display_results)

            best_candidate = screening_results[0]

            st.subheader("Top Candidate Recommendation")

            st.success(
                f"{best_candidate['Candidate Name']} is the top ranked candidate "
                f"with a final screening score of {best_candidate['Final Screening Score']}%."
            )

            missing_skills_for_interview = []

            if best_candidate["Missing Skills"] != "":
                missing_skills_for_interview = best_candidate["Missing Skills"].split(", ")

            interview_report = generate_interview_readiness_report(
                best_candidate["Candidate Name"],
                best_candidate["Job Match Score"],
                best_candidate["Semantic Match Score"],
                missing_skills_for_interview
            )

            st.subheader("Candidate Interview Readiness Report")

            st.metric(
                "Interview Readiness Score",
                f"{interview_report['final_score']}%"
            )

            st.write("**Decision:**", interview_report["decision"])
            st.write("**Missing Skills:**", interview_report["missing_skills"])
            st.info(interview_report["summary"])
            st.success(interview_report["next_step"])

            report_text = "========================================\n"
            report_text += "TalentBridge AI - HR Batch Screening Report\n"
            report_text += "========================================\n\n"

            report_text += "Executive Summary\n"
            report_text += "-----------------\n"
            report_text += (
                "This report compares one job description against multiple candidate resumes. "
                "Candidates are ranked using Job Match Score, Semantic Match Score, and Final Screening Score.\n\n"
            )

            report_text += "Top Candidate\n"
            report_text += "-------------\n"
            report_text += f"Candidate Name: {best_candidate['Candidate Name']}\n"
            report_text += f"Final Screening Score: {best_candidate['Final Screening Score']}%\n"
            report_text += f"Recommendation: {best_candidate['Recommendation']}\n\n"

            report_text += "Ranked Candidate Results\n"
            report_text += "------------------------\n\n"

            for index, candidate in enumerate(screening_results, start=1):
                report_text += f"Rank {index}: {candidate['Candidate Name']}\n"
                report_text += f"Job Match Score: {candidate['Job Match Score']}%\n"
                report_text += f"Semantic Match Score: {candidate['Semantic Match Score']}%\n"
                report_text += f"Final Screening Score: {candidate['Final Screening Score']}%\n"
                report_text += f"Matched Skills: {candidate['Matched Skills']}\n"
                report_text += f"Missing Skills: {candidate['Missing Skills']}\n"
                report_text += f"Strong Evidence Skills: {candidate['Strong Evidence Skills']}\n"
                report_text += f"Weak Evidence Skills: {candidate['Weak Evidence Skills']}\n"
                report_text += f"Recommendation: {candidate['Recommendation']}\n"
               
                report_text += "----------------------------------------\n\n"

            report_text += "Top Candidate Interview Readiness Report\n"
            report_text += "----------------------------------------\n"
            report_text += f"Candidate Name: {interview_report['candidate_name']}\n"
            report_text += f"Interview Readiness Score: {interview_report['final_score']}%\n"
            report_text += f"Decision: {interview_report['decision']}\n"
            report_text += f"Missing Skills: {interview_report['missing_skills']}\n"
            report_text += f"Summary: {interview_report['summary']}\n"
            report_text += f"Recommended Next Step: {interview_report['next_step']}\n\n"

            report_text += "Generated by TalentBridge AI\n"
            report_text += "Career Readiness + Job Matching + Training Pathway\n"
            st.download_button(
                label="Download HR Batch Screening Report",
                data=report_text,
                file_name="talentbridge_hr_batch_screening_report.txt",
                mime="text/plain"
            )

