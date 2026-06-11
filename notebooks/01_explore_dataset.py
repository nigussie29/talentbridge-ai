import pandas as pd
from pathlib import Path

# Find the main project folder
project_folder = Path(__file__).resolve().parent.parent

# Build the full path to the CSV file
csv_file = project_folder / "data" / "career_profiles.csv"

print("Looking for file here:")
print(csv_file)

# Load the dataset
df = pd.read_csv(csv_file)

# Show the first 5 rows
print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns)

print("\nBasic information:")
print(df.info())

print("\nTarget role counts:")
print(df["target_role"].value_counts())

print("\n--- Simple AI Career Recommendation ---")

# Example user profile
user_profile = {
    "python_skill": 4,
    "math_skill": 5,
    "data_skill": 4,
    "ai_skill": 3,
    "communication_skill": 4,
    "experience_years": 2
}

# Simple rule-based recommendation
if user_profile["python_skill"] >= 4 and user_profile["math_skill"] >= 4 and user_profile["ai_skill"] >= 3:
    recommendation = "AI Engineer"
elif user_profile["data_skill"] >= 4 and user_profile["communication_skill"] >= 4:
    recommendation = "Data Analyst or AI Product Analyst"
elif user_profile["communication_skill"] >= 5 and user_profile["ai_skill"] >= 3:
    recommendation = "AI Education Specialist"
else:
    recommendation = "Start with Data Analyst, then move toward AI Engineer"

print("User profile:")
print(user_profile)

print("\nRecommended career path:")
print(recommendation)

print("\n--- Skill Gap Analysis ---")

# Skills required for each career path
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

target_career = "AI Engineer"

print("Target career:", target_career)

gaps = {}

for skill, required_level in required_skills[target_career].items():
    current_level = user_profile[skill]
    gap = required_level - current_level

    if gap > 0:
        gaps[skill] = gap

if len(gaps) == 0:
    print("You are ready for this career path.")
else:
    print("Skills to improve:")
    for skill, gap in gaps.items():
        print(f"- {skill}: improve by {gap} level(s)")

        print("\n--- Recommended Portfolio Projects ---")

# Project recommendations based on missing skills
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

if len(gaps) == 0:
    print("You do not have major skill gaps. Start building an advanced AI portfolio project.")
else:
    for skill in gaps.keys():
        print(f"\nBecause you need to improve {skill}, try these projects:")
        for project in project_recommendations[skill]:
            print(f"- {project}")
            print("\n--- Career Readiness Score ---")

# Calculate readiness score for the target career
target_requirements = required_skills[target_career]

total_score = 0
max_score = 0

for skill, required_level in target_requirements.items():
    current_level = user_profile[skill]

    # If current skill is higher than required, cap it at required level
    skill_score = min(current_level, required_level)

    total_score += skill_score
    max_score += required_level

readiness_score = (total_score / max_score) * 100

print(f"Target career: {target_career}")
print(f"Career readiness score: {readiness_score:.2f}%")

if readiness_score >= 90:
    print("Status: Strong candidate")
elif readiness_score >= 75:
    print("Status: Almost ready")
elif readiness_score >= 60:
    print("Status: Developing candidate")
else:
    print("Status: Beginner level - build more foundation projects")
    print("\n--- Reusable Career Analysis Function ---")

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


result = analyze_career_profile(user_profile, "AI Engineer")

print(result)