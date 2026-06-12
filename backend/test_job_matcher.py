from career_engine import (
    analyze_resume_text,
    analyze_job_description,
    compare_resume_to_job,
    generate_course_plan
)

resume_text = """
I am a Data Analyst with experience in Python, SQL, Power BI,
data analysis, dashboards, data cleaning, communication, and machine learning basics.
"""

job_description = """
We are hiring a Data Analyst. The candidate should have strong SQL, Python,
Power BI, Excel, data visualization, statistics, ETL, and stakeholder communication skills.
Experience with Git and cloud platforms is a plus.
"""

resume_skills = analyze_resume_text(resume_text)
job_required_skills = analyze_job_description(job_description)

comparison = compare_resume_to_job(resume_skills, job_required_skills)
course_plan = generate_course_plan(comparison["missing_skills"])

print("Resume Skills:")
print(resume_skills)

print("\nJob Required Skills:")
print(job_required_skills)

print("\nMatched Skills:")
print(comparison["matched_skills"])

print("\nMissing Skills:")
print(comparison["missing_skills"])

print("\nJob Match Score:")
print(comparison["match_score"], "%")

print("\nPersonalized Course Plan:")
for skill, lessons in course_plan.items():
    print(f"\n{skill}:")
    for lesson in lessons:
        print("-", lesson)