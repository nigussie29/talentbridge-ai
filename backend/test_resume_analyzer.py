from career_engine import analyze_resume_text, create_profile_from_resume, analyze_career_profile

sample_resume = """
I am a computer science teacher with experience in Python, Power BI,
data analysis, dashboards, teaching, and machine learning projects.
I have also worked with AI tools and student learning platforms.
"""

detected_skills = analyze_resume_text(sample_resume)

print("Detected Skills:")
for skill in detected_skills:
    print("-", skill)

profile = create_profile_from_resume(detected_skills)

print("\nEstimated Profile:")
print(profile)

result = analyze_career_profile(profile, "AI Education Specialist")

print("\nCareer Analysis:")
print("Target Career:", result["target_career"])
print("Readiness Score:", result["readiness_score"], "%")
print("Status:", result["status"])
print("Skill Gaps:", result["skill_gaps"])