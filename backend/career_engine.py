# career_engine.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

required_skills = {
    "AI Engineer": {
        "python_skill": 5,
        "math_skill": 4,
        "data_skill": 4,
        "ai_skill": 5,
        "communication_skill": 3
    },
    "Data Analyst": {
        "python_skill": 3,
        "math_skill": 3,
        "data_skill": 5,
        "ai_skill": 2,
        "communication_skill": 4
    },
    "Machine Learning Engineer": {
        "python_skill": 5,
        "math_skill": 5,
        "data_skill": 4,
        "ai_skill": 4,
        "communication_skill": 3
    },
    "AI Education Specialist": {
        "python_skill": 3,
        "math_skill": 3,
        "data_skill": 3,
        "ai_skill": 4,
        "communication_skill": 5
    }
}


project_recommendations = {
    "python_skill": [
        "Build a Python data cleaning project using pandas",
        "Create a command-line resume analyzer",
        "Build a Python calculator for career readiness score"
    ],
    "math_skill": [
        "Build a probability simulation project",
        "Create a linear regression model from scratch",
        "Build a statistics dashboard"
    ],
    "data_skill": [
        "Create a Power BI job market dashboard",
        "Analyze AI job descriptions using pandas",
        "Build a dataset cleaning and visualization project"
    ],
    "ai_skill": [
        "Build a resume feedback chatbot using an LLM",
        "Create a RAG assistant that answers questions from job descriptions",
        "Build a career recommendation machine learning model"
    ],
    "communication_skill": [
        "Create a professional portfolio website",
        "Record a 3-minute project demo video",
        "Write a project case study explaining the business problem"
    ]
}


def analyze_career_profile(user_profile, target_career):
    target_requirements = required_skills[target_career]

    gaps = {}
    total_score = 0
    max_score = 0

    for skill, required_level in target_requirements.items():
        current_level = user_profile[skill]
        gap = required_level - current_level

        if gap > 0:
            gaps[skill] = gap

        skill_score = min(current_level, required_level)
        total_score += skill_score
        max_score += required_level

    readiness_score = (total_score / max_score) * 100

    if readiness_score >= 90:
        status = "Strong candidate"
    elif readiness_score >= 75:
        status = "Almost ready"
    elif readiness_score >= 60:
        status = "Developing candidate"
    else:
        status = "Beginner level - build more foundation projects"

    recommended_projects = {}

    for skill in gaps.keys():
        recommended_projects[skill] = project_recommendations[skill]

        return {
        "target_career": target_career,
        "readiness_score": round(readiness_score, 2),
        "status": status,
        "skill_gaps": gaps,
        "recommended_projects": recommended_projects
    }

def analyze_resume_text(resume_text):
    skill_keywords = {
        "Python": [
            "python", "pandas", "numpy", "matplotlib", "seaborn",
            "dataframe", "jupyter", "google colab", "scripting",
            "automation with python"
        ],

        "SQL": [
            "sql", "database", "mysql", "postgresql", "sqlite",
            "query", "queries", "joins", "tables", "relational database",
            "data warehouse"
        ],

        "Power BI": [
            "power bi", "dashboard", "dashboards", "dax",
            "power query", "business intelligence", "bi report",
            "data model", "kpi", "visual report"
        ],

        "Excel": [
            "excel", "spreadsheet", "pivot table", "vlookup",
            "xlookup", "worksheet", "formulas", "charts"
        ],

        "Statistics": [
            "statistics", "statistical analysis", "probability",
            "hypothesis testing", "regression", "correlation",
            "mean", "median", "standard deviation", "variance"
        ],

        "ETL": [
            "etl", "extract", "transform", "load", "data pipeline",
            "pipeline", "data cleaning", "data transformation",
            "data preprocessing", "data wrangling"
        ],

        "Git": [
            "git", "github", "version control", "repository",
            "commit", "push", "pull request"
        ],

        "Cloud": [
            "cloud", "azure", "aws", "google cloud", "gcp",
            "cloud storage", "cloud database", "microsoft fabric"
        ],

        "Machine Learning": [
            "machine learning", "scikit-learn", "sklearn",
            "model training", "classification", "regression model",
            "predictive model", "supervised learning",
            "unsupervised learning", "random forest",
            "decision tree", "logistic regression"
        ],

        "Artificial Intelligence": [
            "artificial intelligence", "ai", "llm", "rag",
            "chatbot", "generative ai", "prompt engineering",
            "openai", "large language model"
        ],

        "Data Analysis": [
            "data analysis", "analyze data", "data cleaning",
            "data visualization", "exploratory data analysis",
            "eda", "insights", "business insights",
            "reporting", "trend analysis"
        ],

        "Data Visualization": [
            "data visualization", "visualization", "charts",
            "graphs", "plot", "dashboard", "matplotlib",
            "power bi", "tableau"
        ],

        "Communication": [
            "communication", "presentation", "presented",
            "stakeholder", "stakeholders", "training",
            "teaching", "explained", "report writing",
            "business report"
        ]
    }

    resume_text_lower = resume_text.lower()
    detected_skills = []

    for skill, keywords in skill_keywords.items():
        for keyword in keywords:
            if keyword in resume_text_lower:
                detected_skills.append(skill)
                break

    return detected_skills
def create_profile_from_resume(detected_skills):
    profile = {
        "python_skill": 1,
        "math_skill": 1,
        "data_skill": 1,
        "ai_skill": 1,
        "communication_skill": 1,
        "experience_years": 0
    }

    if "Python" in detected_skills:
        profile["python_skill"] = 3

    if "SQL" in detected_skills:
        profile["data_skill"] = max(profile["data_skill"], 3)

    if "Power BI" in detected_skills:
        profile["data_skill"] = max(profile["data_skill"], 4)

    if "Data Analysis" in detected_skills:
        profile["data_skill"] = max(profile["data_skill"], 4)

    if "Machine Learning" in detected_skills:
        profile["ai_skill"] = max(profile["ai_skill"], 3)
        profile["math_skill"] = max(profile["math_skill"], 3)

    if "Artificial Intelligence" in detected_skills:
        profile["ai_skill"] = max(profile["ai_skill"], 3)

    if "Communication" in detected_skills:
        profile["communication_skill"] = 4

    return profile
def generate_text_report(result, skill_display_names=None):
    if skill_display_names is None:
        skill_display_names = {}

    report = ""

    report += "--- TalentBridge AI Career Report ---\n\n"
    report += f"Target Career: {result['target_career']}\n"
    report += f"Readiness Score: {result['readiness_score']}%\n"
    report += f"Status: {result['status']}\n"

    report += "\nSkill Gaps:\n"

    if len(result["skill_gaps"]) == 0:
        report += "No major skill gaps. You are ready to build advanced projects.\n"
    else:
        for skill, gap in result["skill_gaps"].items():
            clean_skill_name = skill_display_names.get(skill, skill)
            report += f"- {clean_skill_name}: improve by {gap} level(s)\n"

    report += "\nRecommended Portfolio Projects:\n"

    if len(result["recommended_projects"]) == 0:
        report += "Build an advanced end-to-end AI portfolio project.\n"
    else:
        for skill, projects in result["recommended_projects"].items():
            clean_skill_name = skill_display_names.get(skill, skill)
            report += f"\nFor {clean_skill_name}:\n"
            for project in projects:
                report += f"- {project}\n"

    return report
def analyze_job_description(job_description_text):
    skill_keywords = {
        "Python": ["python", "pandas", "numpy"],
        "SQL": ["sql", "database", "mysql", "postgresql"],
        "Power BI": ["power bi", "dashboard", "dax"],
        "Machine Learning": ["machine learning", "scikit-learn", "model training"],
        "Artificial Intelligence": ["artificial intelligence", "ai", "llm", "rag", "chatbot"],
        "Data Analysis": ["data analysis", "data cleaning", "data visualization"],
        "Communication": ["communication", "presentation", "stakeholder", "reporting"],
        "Excel": ["excel", "spreadsheet", "pivot table"],
        "Statistics": ["statistics", "probability", "statistical analysis"],
        "ETL": ["etl", "data pipeline", "data transformation"],
        "Cloud": ["aws", "azure", "gcp", "cloud"],
        "FastAPI": ["fastapi", "api", "rest api"],
        "Streamlit": ["streamlit"],
        "Git": ["git", "github", "version control"]
    }

    job_description_lower = job_description_text.lower()
    required_skills = []

    for skill, keywords in skill_keywords.items():
        for keyword in keywords:
            if keyword in job_description_lower:
                required_skills.append(skill)
                break

    return required_skills


def compare_resume_to_job(resume_skills, job_required_skills):
    matched_skills = []
    missing_skills = []

    for skill in job_required_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if len(job_required_skills) == 0:
        match_score = 0
    else:
        match_score = (len(matched_skills) / len(job_required_skills)) * 100

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": round(match_score, 2)
    }
def generate_course_plan(missing_skills):
    course_library = {
        "Excel": [
            "Learn Excel formulas, tables, sorting, filtering, and pivot tables.",
            "Practice cleaning a messy spreadsheet dataset.",
            "Create one Excel dashboard and explain your findings."
        ],
        "Statistics": [
            "Review mean, median, standard deviation, probability, and correlation.",
            "Practice interpreting charts and summary statistics.",
            "Complete a small statistics project using real data."
        ],
        "ETL": [
            "Learn what Extract, Transform, Load means.",
            "Practice cleaning and transforming CSV data using Python pandas.",
            "Build a small ETL pipeline from raw data to clean report."
        ],
        "Cloud": [
            "Learn basic cloud concepts: storage, compute, database, and deployment.",
            "Compare AWS, Azure, and Google Cloud at a beginner level.",
            "Deploy one small app or dashboard online."
        ],
        "Git": [
            "Learn Git basics: init, add, commit, status, branch, and push.",
            "Create a GitHub repository for a portfolio project.",
            "Write a professional README.md file."
        ],
        "SQL": [
            "Learn SELECT, WHERE, ORDER BY, GROUP BY, and JOIN.",
            "Practice writing queries on a sample database.",
            "Create a mini SQL analysis project."
        ],
        "Python": [
            "Review Python variables, lists, dictionaries, functions, and loops.",
            "Practice pandas data analysis.",
            "Build a Python project and upload it to GitHub."
        ],
        "Power BI": [
            "Learn Power BI visuals, filters, slicers, and measures.",
            "Practice Power Query data cleaning.",
            "Create a business dashboard project."
        ],
        "Machine Learning": [
            "Learn supervised learning, features, labels, training, and testing.",
            "Build a classification model using a simple dataset.",
            "Explain model accuracy and limitations."
        ],
        "Artificial Intelligence": [
            "Learn AI concepts: LLMs, prompts, RAG, embeddings, and chatbots.",
            "Build a simple AI assistant project.",
            "Document ethical risks and limitations."
        ],
        "Data Analysis": [
            "Learn data cleaning, grouping, filtering, and visualization.",
            "Analyze a real dataset using Python or Power BI.",
            "Write a short report explaining insights."
        ],
        "Communication": [
            "Practice explaining technical results in simple language.",
            "Create a one-page project summary.",
            "Record a short presentation explaining your portfolio project."
        ]
    }

    course_plan = {}

    for skill in missing_skills:
        if skill in course_library:
            course_plan[skill] = course_library[skill]
        else:
            course_plan[skill] = [
                f"Study the basics of {skill}.",
                f"Complete one practice activity using {skill}.",
                f"Build a small portfolio project showing {skill}."
            ]

    return course_plan
def generate_hr_report(job_comparison):
    match_score = job_comparison["match_score"]
    matched_skills = job_comparison["matched_skills"]
    missing_skills = job_comparison["missing_skills"]

    if match_score >= 80:
        recommendation = "Interview Ready"
        decision = "Recommend for interview"
        summary = (
            "This candidate shows strong alignment with the job requirements. "
            "The candidate has most of the required skills and appears ready for the interview stage."
        )
    elif match_score >= 50:
        recommendation = "Train Before Interview"
        decision = "Recommend targeted training before final interview"
        summary = (
            "This candidate has a useful foundation but is not fully ready yet. "
            "The candidate should complete targeted training in the missing skills before moving forward."
        )
    else:
        recommendation = "Not Ready Yet"
        decision = "Recommend learning pathway before interview consideration"
        summary = (
            "This candidate has a low match with the current job requirements. "
            "The candidate should complete a structured learning plan and build portfolio evidence before applying."
        )

    report = {
        "recommendation": recommendation,
        "decision": decision,
        "match_score": match_score,
        "strengths": matched_skills,
        "skill_gaps": missing_skills,
        "summary": summary
    }

    return report
def generate_mode_report(user_mode, job_comparison, hr_report):
    matched_skills = job_comparison["matched_skills"]
    missing_skills = job_comparison["missing_skills"]
    match_score = job_comparison["match_score"]

    report = ""
    report += "TalentBridge AI Full Report\n"
    report += "===========================\n\n"
    report += f"User Mode: {user_mode}\n"
    report += f"Job Match Score: {match_score}%\n\n"

    report += "Matched Skills:\n"
    if len(matched_skills) == 0:
        report += "- No matched skills found.\n"
    else:
        for skill in matched_skills:
            report += f"- {skill}\n"

    report += "\nMissing Skills:\n"
    if len(missing_skills) == 0:
        report += "- No missing skills. Strong match.\n"
    else:
        for skill in missing_skills:
            report += f"- {skill}\n"

    if user_mode == "Job Seeker":
        report += "\nPersonalized Course Plan:\n"
        course_plan = generate_course_plan(missing_skills)

        if len(missing_skills) == 0:
            report += "- You are a strong match. Start preparing for interviews.\n"
        else:
            for skill, lessons in course_plan.items():
                report += f"\n{skill}:\n"
                for lesson in lessons:
                    report += f"- {lesson}\n"

        report += "\nPortfolio Evidence Checklist:\n"
        if len(missing_skills) == 0:
            report += "- Add your best 1–2 portfolio projects to your resume.\n"
            report += "- Prepare interview stories for your strongest skills.\n"
        else:
            for skill in missing_skills:
                report += f"- Build one small project that proves your {skill} skill.\n"

    elif user_mode == "HR / Recruiter":
        report += "\nHR Candidate Report:\n"
        report += f"Candidate Recommendation: {hr_report['recommendation']}\n"
        report += f"HR Decision: {hr_report['decision']}\n"
        report += f"HR Summary: {hr_report['summary']}\n"

    else:
        report += "\nTraining Center Learning Pathway:\n"
        course_plan = generate_course_plan(missing_skills)

        if len(missing_skills) == 0:
            report += "- This learner is ready for advanced placement or interview preparation.\n"
        else:
            week_number = 1
            for skill, lessons in course_plan.items():
                report += f"\nWeek {week_number}: {skill}\n"
                for lesson in lessons:
                    report += f"- {lesson}\n"
                week_number += 1

    return report
def generate_progress_tracker(missing_skills):
    evidence_library = {
        "Excel": {
            "learning_task": "Create an Excel dashboard using formulas, filters, and pivot tables.",
            "portfolio_evidence": "Upload a dashboard screenshot or Excel project summary.",
            "status": "Not Started"
        },
        "Statistics": {
            "learning_task": "Complete a mini statistics analysis using mean, median, standard deviation, and correlation.",
            "portfolio_evidence": "Upload a short statistics report or notebook.",
            "status": "Not Started"
        },
        "ETL": {
            "learning_task": "Build a small ETL pipeline that extracts, cleans, transforms, and saves data.",
            "portfolio_evidence": "Upload a GitHub link showing the ETL pipeline.",
            "status": "Not Started"
        },
        "Cloud": {
            "learning_task": "Deploy a small app, dashboard, or API online.",
            "portfolio_evidence": "Add a live app link or deployment screenshot.",
            "status": "Not Started"
        },
        "Git": {
            "learning_task": "Create a GitHub repository and push one complete project.",
            "portfolio_evidence": "Add the GitHub repository link.",
            "status": "Not Started"
        },
        "SQL": {
            "learning_task": "Write SQL queries using SELECT, WHERE, GROUP BY, JOIN, and ORDER BY.",
            "portfolio_evidence": "Upload SQL query examples or a database analysis project.",
            "status": "Not Started"
        },
        "Python": {
            "learning_task": "Build a Python project using functions, dictionaries, pandas, and file handling.",
            "portfolio_evidence": "Upload the Python project to GitHub.",
            "status": "Not Started"
        },
        "Power BI": {
            "learning_task": "Create a Power BI dashboard with visuals, filters, and business insights.",
            "portfolio_evidence": "Upload dashboard screenshots or a Power BI project summary.",
            "status": "Not Started"
        },
        "Machine Learning": {
            "learning_task": "Train and evaluate a simple classification or regression model.",
            "portfolio_evidence": "Upload a notebook showing model training, accuracy, and explanation.",
            "status": "Not Started"
        },
        "Artificial Intelligence": {
            "learning_task": "Build a simple AI assistant, prompt system, or RAG prototype.",
            "portfolio_evidence": "Upload the AI app link, GitHub repo, or project write-up.",
            "status": "Not Started"
        },
        "Data Analysis": {
            "learning_task": "Analyze a real dataset and explain insights with charts.",
            "portfolio_evidence": "Upload a notebook, dashboard, or written analysis report.",
            "status": "Not Started"
        },
        "Communication": {
            "learning_task": "Create a one-page project summary and explain results clearly.",
            "portfolio_evidence": "Upload a project summary or short presentation.",
            "status": "Not Started"
        }
    }

    tracker = []

    for skill in missing_skills:
        if skill in evidence_library:
            tracker.append({
                "Missing Skill": skill,
                "Learning Task": evidence_library[skill]["learning_task"],
                "Portfolio Evidence": evidence_library[skill]["portfolio_evidence"],
                "Status": evidence_library[skill]["status"]
            })
        else:
            tracker.append({
                "Missing Skill": skill,
                "Learning Task": f"Study the basics of {skill}.",
                "Portfolio Evidence": f"Build one small project proving {skill}.",
                "Status": "Not Started"
            })

    return tracker
def generate_progress_tracker(missing_skills):
    evidence_library = {
        "Excel": {
            "learning_task": "Create an Excel dashboard using formulas, filters, and pivot tables.",
            "portfolio_evidence": "Upload a dashboard screenshot or Excel project summary.",
            "status": "Not Started"
        },
        "Statistics": {
            "learning_task": "Complete a mini statistics analysis using mean, median, standard deviation, and correlation.",
            "portfolio_evidence": "Upload a short statistics report or notebook.",
            "status": "Not Started"
        },
        "ETL": {
            "learning_task": "Build a small ETL pipeline that extracts, cleans, transforms, and saves data.",
            "portfolio_evidence": "Upload a GitHub link showing the ETL pipeline.",
            "status": "Not Started"
        },
        "Cloud": {
            "learning_task": "Deploy a small app, dashboard, or API online.",
            "portfolio_evidence": "Add a live app link or deployment screenshot.",
            "status": "Not Started"
        },
        "Git": {
            "learning_task": "Create a GitHub repository and push one complete project.",
            "portfolio_evidence": "Add the GitHub repository link.",
            "status": "Not Started"
        },
        "SQL": {
            "learning_task": "Write SQL queries using SELECT, WHERE, GROUP BY, JOIN, and ORDER BY.",
            "portfolio_evidence": "Upload SQL query examples or a database analysis project.",
            "status": "Not Started"
        },
        "Python": {
            "learning_task": "Build a Python project using functions, dictionaries, pandas, and file handling.",
            "portfolio_evidence": "Upload the Python project to GitHub.",
            "status": "Not Started"
        },
        "Power BI": {
            "learning_task": "Create a Power BI dashboard with visuals, filters, and business insights.",
            "portfolio_evidence": "Upload dashboard screenshots or a Power BI project summary.",
            "status": "Not Started"
        },
        "Machine Learning": {
            "learning_task": "Train and evaluate a simple classification or regression model.",
            "portfolio_evidence": "Upload a notebook showing model training, accuracy, and explanation.",
            "status": "Not Started"
        },
        "Artificial Intelligence": {
            "learning_task": "Build a simple AI assistant, prompt system, or RAG prototype.",
            "portfolio_evidence": "Upload the AI app link, GitHub repo, or project write-up.",
            "status": "Not Started"
        },
        "Data Analysis": {
            "learning_task": "Analyze a real dataset and explain insights with charts.",
            "portfolio_evidence": "Upload a notebook, dashboard, or written analysis report.",
            "status": "Not Started"
        },
        "Communication": {
            "learning_task": "Create a one-page project summary and explain results clearly.",
            "portfolio_evidence": "Upload a project summary or short presentation.",
            "status": "Not Started"
        }
    }

    tracker = []

    for skill in missing_skills:
        if skill in evidence_library:
            tracker.append({
                "Missing Skill": skill,
                "Learning Task": evidence_library[skill]["learning_task"],
                "Portfolio Evidence": evidence_library[skill]["portfolio_evidence"],
                "Status": evidence_library[skill]["status"]
            })
        else:
            tracker.append({
                "Missing Skill": skill,
                "Learning Task": f"Study the basics of {skill}.",
                "Portfolio Evidence": f"Build one small project proving {skill}.",
                "Status": "Not Started"
            })

    return tracker
def calculate_improvement_score(job_comparison):
    current_score = job_comparison["match_score"]
    missing_skills = job_comparison["missing_skills"]

    # Simple rule:
    # each missing skill completed can improve readiness by 6 points
    possible_improvement = len(missing_skills) * 6

    estimated_score = current_score + possible_improvement

    if estimated_score > 100:
        estimated_score = 100

    improvement_potential = estimated_score - current_score

    if current_score >= 80:
        current_status = "Interview Ready"
    elif current_score >= 50:
        current_status = "Train Before Interview"
    else:
        current_status = "Not Ready Yet"

    if estimated_score >= 80:
        estimated_status = "Interview Ready"
    elif estimated_score >= 50:
        estimated_status = "Train Before Interview"
    else:
        estimated_status = "Not Ready Yet"

    return {
        "current_score": round(current_score, 2),
        "estimated_score_after_training": round(estimated_score, 2),
        "improvement_potential": round(improvement_potential, 2),
        "current_status": current_status,
        "estimated_status_after_training": estimated_status
    }
def prioritize_missing_skills(missing_skills):
    high_priority = [
        "Python",
        "SQL",
        "ETL",
        "Machine Learning",
        "Statistics",
        "Artificial Intelligence"
    ]

    medium_priority = [
        "Git",
        "Cloud",
        "Power BI",
        "Excel",
        "Data Visualization",
        "Data Analysis"
    ]

    priority_report = []

    for skill in missing_skills:
        if skill in high_priority:
            priority = "High Priority"
        elif skill in medium_priority:
            priority = "Medium Priority"
        else:
            priority = "Low Priority"

        priority_report.append(
            {
                "Missing Skill": skill,
                "Priority Level": priority
            }
        )

    return priority_report
def calculate_semantic_match_score(resume_text, job_description_text):
    texts = [
        resume_text,
        job_description_text
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(texts)

    similarity_score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    semantic_score = round(similarity_score * 100, 2)

    return semantic_score
calculate_semantic_match_score = calculate_semantic_match_score
def calculate_proof_based_readiness_score(
    job_match_score,
    semantic_match_score,
    evidence_links,
    progress_statuses
):
    total_skills = len(progress_statuses)

    if total_skills == 0:
        portfolio_evidence_score = 100
        progress_completion_score = 100
    else:
        completed_evidence_count = 0
        completed_progress_count = 0

        for skill in progress_statuses:
            evidence_link = evidence_links.get(skill, "")
            progress_status = progress_statuses.get(skill, "Not Started")

            if evidence_link.strip() != "":
                completed_evidence_count += 1

            if progress_status == "Completed":
                completed_progress_count += 1

        portfolio_evidence_score = round(
            (completed_evidence_count / total_skills) * 100,
            2
        )

        progress_completion_score = round(
            (completed_progress_count / total_skills) * 100,
            2
        )

    proof_based_score = round(
        (job_match_score * 0.40)
        + (semantic_match_score * 0.20)
        + (portfolio_evidence_score * 0.25)
        + (progress_completion_score * 0.15),
        2
    )

    if proof_based_score >= 85:
        readiness_level = "Strong Proof of Readiness"
    elif proof_based_score >= 70:
        readiness_level = "Good Proof, Needs Minor Improvement"
    elif proof_based_score >= 50:
        readiness_level = "Developing Proof"
    else:
        readiness_level = "Weak Proof, Needs Portfolio Evidence"

    return {
        "proof_based_score": proof_based_score,
        "portfolio_evidence_score": portfolio_evidence_score,
        "progress_completion_score": progress_completion_score,
        "readiness_level": readiness_level
    }
def calculate_proof_based_readiness_score(
    job_match_score,
    semantic_match_score,
    evidence_links,
    progress_statuses
):
    total_skills = len(progress_statuses)

    if total_skills == 0:
        portfolio_evidence_score = 100
        progress_completion_score = 100
    else:
        completed_evidence_count = 0
        completed_progress_count = 0

        for skill in progress_statuses:
            evidence_link = evidence_links.get(skill, "")
            progress_status = progress_statuses.get(skill, "Not Started")

            if evidence_link.strip() != "":
                completed_evidence_count += 1

            if progress_status == "Completed":
                completed_progress_count += 1

        portfolio_evidence_score = round(
            (completed_evidence_count / total_skills) * 100,
            2
        )

        progress_completion_score = round(
            (completed_progress_count / total_skills) * 100,
            2
        )

    proof_based_score = round(
        (job_match_score * 0.40)
        + (semantic_match_score * 0.20)
        + (portfolio_evidence_score * 0.25)
        + (progress_completion_score * 0.15),
        2
    )

    if proof_based_score >= 85:
        readiness_level = "Strong Proof of Readiness"
    elif proof_based_score >= 70:
        readiness_level = "Good Proof, Needs Minor Improvement"
    elif proof_based_score >= 50:
        readiness_level = "Developing Proof"
    else:
        readiness_level = "Weak Proof, Needs Portfolio Evidence"

    return {
        "proof_based_score": proof_based_score,
        "portfolio_evidence_score": portfolio_evidence_score,
        "progress_completion_score": progress_completion_score,
        "readiness_level": readiness_level
    }
def screen_multiple_candidates(job_description_text, candidate_resumes):
    job_required_skills = analyze_job_description(job_description_text)

    screening_results = []

    for candidate in candidate_resumes:
        candidate_name = candidate.get("candidate_name", "Unknown Candidate")
        resume_text = candidate.get("resume_text", "")

        resume_skills = analyze_resume_text(resume_text)

        job_comparison = compare_resume_to_job(
            resume_skills,
            job_required_skills
        )

        semantic_score = calculate_semantic_match_score(
            resume_text,
            job_description_text
        )

        final_screening_score = round(
            (job_comparison["match_score"] * 0.60)
            + (semantic_score * 0.40),
            2
        )

        if final_screening_score >= 85:
            recommendation = "Strong Interview Candidate"
        elif final_screening_score >= 70:
            recommendation = "Interview After Quick Review"
        elif final_screening_score >= 50:
            recommendation = "Train Before Interview"
        else:
            recommendation = "Not Ready Yet"

        screening_results.append(
            {
                "Candidate Name": candidate_name,
                "Job Match Score": job_comparison["match_score"],
                "Semantic Match Score": semantic_score,
                "Final Screening Score": final_screening_score,
                "Matched Skills": ", ".join(job_comparison["matched_skills"]),
                "Missing Skills": ", ".join(job_comparison["missing_skills"]),
                "Recommendation": recommendation
            }
        )

    screening_results = sorted(
        screening_results,
        key=lambda x: x["Final Screening Score"],
        reverse=True
    )

    return screening_results