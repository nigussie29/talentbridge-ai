from career_engine import analyze_career_profile
skill_display_names = {
    "python_skill": "Python Skill",
    "math_skill": "Mathematics Skill",
    "data_skill": "Data Analysis Skill",
    "ai_skill": "Artificial Intelligence Skill",
    "communication_skill": "Communication Skill"
}

print("Welcome to TalentBridge AI Career Analyzer")
print("Answer each skill from 1 to 5")
print("1 = beginner, 5 = advanced\n")

def get_skill_input(skill_name):
    while True:
        try:
            value = int(input(f"{skill_name} skill level (1-5): "))

            if value >= 1 and value <= 5:
                return value
            else:
                print("Please enter a number from 1 to 5.")

        except ValueError:
            print("Invalid input. Please enter a number.")


def get_experience_input():
    while True:
        try:
            value = int(input("Years of experience: "))

            if value >= 0:
                return value
            else:
                print("Experience cannot be negative.")

        except ValueError:
            print("Invalid input. Please enter a number.")


python_skill = get_skill_input("Python")
math_skill = get_skill_input("Math")
data_skill = get_skill_input("Data")
ai_skill = get_skill_input("AI")
communication_skill = get_skill_input("Communication")
experience_years = get_experience_input()

print("\nChoose your target career:")
print("1. AI Engineer")
print("2. Data Analyst")
print("3. Machine Learning Engineer")
print("4. AI Education Specialist")

choice = input("Enter number 1-4: ")

if choice == "1":
    target_career = "AI Engineer"
elif choice == "2":
    target_career = "Data Analyst"
elif choice == "3":
    target_career = "Machine Learning Engineer"
elif choice == "4":
    target_career = "AI Education Specialist"
else:
    target_career = "AI Engineer"

user_profile = {
    "python_skill": python_skill,
    "math_skill": math_skill,
    "data_skill": data_skill,
    "ai_skill": ai_skill,
    "communication_skill": communication_skill,
    "experience_years": experience_years
}

result = analyze_career_profile(user_profile, target_career)

print("\n--- Career Analysis Result ---")
print("Target Career:", result["target_career"])
print("Readiness Score:", result["readiness_score"], "%")
print("Status:", result["status"])

print("\nSkill Gaps:")
if len(result["skill_gaps"]) == 0:
    print("No major skill gaps. You are ready to build advanced projects.")
else:
    for skill, gap in result["skill_gaps"].items():
      clean_skill_name = skill_display_names.get(skill, skill)
      print(f"- {clean_skill_name}: improve by {gap} level(s)")

print("\nRecommended Projects:")
if len(result["recommended_projects"]) == 0:
    print("Build an advanced end-to-end AI portfolio project.")
else:
    for skill, projects in result["recommended_projects"].items():
        clean_skill_name = skill_display_names.get(skill, skill)
        print(f"\nFor {clean_skill_name}:")
        for project in projects:
            print(f"- {project}")


with open("career_report.txt", "w") as file:
    file.write("--- Career Analysis Result ---\n")
    file.write(f"Target Career: {result['target_career']}\n")
    file.write(f"Readiness Score: {result['readiness_score']}%\n")
    file.write(f"Status: {result['status']}\n")

    file.write("\nSkill Gaps:\n")
    if len(result["skill_gaps"]) == 0:
        file.write("No major skill gaps. You are ready to build advanced projects.\n")
    else:
        for skill, gap in result["skill_gaps"].items():
            clean_skill_name = skill_display_names.get(skill, skill)
            file.write(f"- {clean_skill_name}:improve by {gap} level(s)\n")

    file.write("\nRecommended Projects:\n")
    if len(result["recommended_projects"]) == 0:
        file.write("Build an advanced end-to-end AI portfolio project.\n")
    else:
        for skill, projects in result["recommended_projects"].items():
           clean_skill_name = skill_display_names.get(skill, skill)

        for project in projects:
                file.write(f"- {project}\n")

print("\nReport saved as career_report.txt")