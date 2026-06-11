# career_engine.py

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
        "Python": ["python", "pandas", "numpy"],
        "SQL": ["sql", "database", "mysql", "postgresql"],
        "Power BI": ["power bi", "dashboard", "dax"],
        "Machine Learning": ["machine learning", "scikit-learn", "model training"],
        "Artificial Intelligence": ["artificial intelligence", "ai", "llm", "rag", "chatbot"],
        "Data Analysis": ["data analysis", "data cleaning", "data visualization"],
        "Communication": ["teaching", "presentation", "training", "communication"]
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