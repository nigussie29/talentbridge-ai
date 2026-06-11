# TalentBridge AI Career Analyzer

TalentBridge AI is an end-to-end AI career readiness application that helps users analyze their skills, detect skills from resume text, calculate career readiness, identify skill gaps, and receive personalized portfolio project recommendations.

This project was built as a professional AI/data portfolio project for job search preparation in the AI industry.

---

## Project Overview

Many students, teachers, career changers, and early-career professionals want to enter the AI and data industry but do not know what skills they are missing.

TalentBridge AI solves this problem by allowing users to:

* Paste resume text
* Detect technical and communication skills
* Estimate skill levels from resume content
* Choose a target career
* Calculate a readiness score
* Identify skill gaps
* Receive recommended portfolio projects
* Download a personalized career report

---

## Target Careers

The app currently supports:

* AI Engineer
* Data Analyst
* Machine Learning Engineer
* AI Education Specialist

---

## Key Features

### Resume Skill Analyzer

Users can paste resume text, and the app detects skills such as:

* Python
* SQL
* Power BI
* Machine Learning
* Artificial Intelligence
* Data Analysis
* Communication

### Resume-Based Career Readiness

The app converts detected resume skills into estimated skill levels and compares them to the selected target career.

### Manual Skill Analyzer

Users can manually rate their skill levels using sliders.

### Skill Gap Analysis

The app identifies which skills need improvement.

### Portfolio Project Recommendation

The app recommends projects based on missing skills.

### Downloadable Report

Users can download a personalized career report as a text file.

---

## Tools and Technologies

* Python
* Pandas
* Streamlit
* pathlib
* Basic rule-based AI logic
* Resume keyword extraction
* Skill-gap analysis
* Career readiness scoring

---

## Project Structure

```text
talentbridge-ai/
│
├── backend/
│   ├── career_engine.py
│   ├── interactive_career_app.py
│   ├── test_career_engine.py
│   ├── test_resume_analyzer.py
│   └── career_report.txt
│
├── data/
│   └── career_profiles.csv
│
├── frontend/
│   └── app.py
│
├── notebooks/
│   └── 01_explore_dataset.py
│
├── models/
├── docs/
├── dashboard/
└── README.md
```

---

## How to Run the Project

### 1. Clone or open the project folder

```powershell
cd C:\Users\nigus\OneDrive\Desktop\talentbridge-ai
```

### 2. Install required packages

```powershell
c:\python314\python.exe -m pip install pandas streamlit
```

### 3. Test the backend

```powershell
cd C:\Users\nigus\OneDrive\Desktop\talentbridge-ai\backend
c:\python314\python.exe test_resume_analyzer.py
```

### 4. Run the Streamlit app

```powershell
cd C:\Users\nigus\OneDrive\Desktop\talentbridge-ai\frontend
c:\python314\python.exe -m streamlit run app.py
```

### 5. Open the app

```text
http://localhost:8501
```

---

## Sample Resume Text for Testing

```text
I am a Data Analyst with experience in Python, SQL, Power BI, data analysis, dashboards, data cleaning, data visualization, communication, presentation, and machine learning basics.
```

Expected detected skills:

* Python
* SQL
* Power BI
* Machine Learning
* Data Analysis
* Communication

---

## Example Output

For a Data Analyst target role, the app may show:

```text
Resume Readiness Score: 94.12%
Status: Strong candidate

Skill Gap:
- Data Analysis Skill: improve by 1 level

Recommended Project:
- Create a Power BI job market dashboard
- Analyze AI job descriptions using pandas
- Build a dataset cleaning and visualization project
```

---

## What I Learned

Through this project, I practiced:

* Building a Python backend
* Creating reusable functions
* Reading and analyzing datasets
* Detecting skills from resume text
* Creating a rule-based AI recommendation system
* Building a Streamlit web app
* Debugging Python indentation and import errors
* Organizing a project for GitHub and portfolio use

---

## Future Improvements

Planned improvements include:

* Add PDF resume upload
* Add machine learning model for career prediction
* Add job-description matching
* Add RAG assistant for job and scholarship documents
* Add user login
* Add database storage
* Add Power BI dashboard
* Deploy the app online using Streamlit Cloud

---

## Resume Bullet Point

Built TalentBridge AI, an end-to-end AI career readiness web application using Python and Streamlit. Developed backend logic to analyze resume text, detect skills, estimate skill levels, calculate career readiness scores, identify skill gaps, recommend personalized portfolio projects, and generate downloadable career reports.

---

## Project Status

Current version: Version 1.0
Status: Working local Streamlit app
