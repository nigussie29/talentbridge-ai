from career_engine import analyze_career_profile

user_profile = {
    "python_skill": 4,
    "math_skill": 5,
    "data_skill": 4,
    "ai_skill": 3,
    "communication_skill": 4,
    "experience_years": 2
}

result = analyze_career_profile(user_profile, "AI Engineer")

print("\n--- Career Analysis Result ---")
print("Target Career:", result["target_career"])
print("Readiness Score:", result["readiness_score"], "%")
print("Status:", result["status"])

print("\nSkill Gaps:")
for skill, gap in result["skill_gaps"].items():
    print(f"- {skill}: improve by {gap} level(s)")

print("\nRecommended Projects:")
for skill, projects in result["recommended_projects"].items():
    print(f"\nFor {skill}:")
    for project in projects:
        print(f"- {project}")
        # Save result to a text file
with open("career_report.txt", "w") as file:
    file.write("--- Career Analysis Result ---\n")
    file.write(f"Target Career: {result['target_career']}\n")
    file.write(f"Readiness Score: {result['readiness_score']}%\n")
    file.write(f"Status: {result['status']}\n")

    file.write("\nSkill Gaps:\n")
    for skill, gap in result["skill_gaps"].items():
        file.write(f"- {skill}: improve by {gap} level(s)\n")

    file.write("\nRecommended Projects:\n")
    for skill, projects in result["recommended_projects"].items():
        file.write(f"\nFor {skill}:\n")
        for project in projects:
            file.write(f"- {project}\n")

print("\nReport saved as career_report.txt")