# TalentBridge AI Career Analyzer

## Live Demo

Try the app here:

https://talentbridge-ai-8e3fcvn6dzewqfbskts8dn.streamlit.app/

## GitHub Repository

https://github.com/nigussie29/talentbridge-ai

---

## Project Overview

TalentBridge AI is an AI-powered career readiness and training platform. It helps job seekers, HR teams, recruiters, training centers, students, teachers, career changers, and early-career professionals understand whether a candidate is ready for a target role.

Many people want to enter the AI and data industry but do not know what skills they are missing. Many HR teams also need a clearer way to evaluate whether a candidate should be interviewed, trained, or guided through a learning path.

TalentBridge AI solves this problem by allowing users to:

* Upload a resume PDF
* Paste resume text
* Paste a job description
* Detect technical and communication skills
* Detect job-required skills
* Compare resume skills with job requirements
* Calculate a job match score
* Identify matched and missing skills
* Generate a personalized course plan
* Generate a portfolio evidence checklist
* Generate an HR candidate report
* Generate a training center learning pathway
* Download full reports
* Analyze career readiness manually or from resume text

This project was built as a professional AI/data portfolio project and as the foundation for a marketable career readiness platform.

---

## Product Vision

TalentBridge AI is more than a resume scanner.

It is designed to become a career readiness and training system that answers three important questions:

```text
Is this person ready for the job?
If not, what skills are missing?
What learning path will help this person become ready?
```

The long-term goal is to support:

* Job seekers preparing for AI and data roles
* HR teams screening candidates
* Training centers building student learning pathways
* Career changers moving into technology roles
* Schools and workforce programs preparing learners for real jobs

---

## User Modes

TalentBridge AI currently supports three user modes.

### Job Seeker Mode

Job Seeker Mode helps users:

* Compare their resume with a job description
* See their job match score
* Identify missing skills
* Receive a personalized course plan
* Receive a portfolio evidence checklist
* Download a full job seeker report

### HR / Recruiter Mode

HR / Recruiter Mode helps recruiters and hiring teams:

* Compare candidate resumes with job descriptions
* Identify candidate strengths
* Identify candidate skill gaps
* Generate an HR candidate report
* Decide whether a candidate is interview-ready, needs training, or is not ready yet
* Download a full HR-style candidate report

### Training Center Mode

Training Center Mode helps schools, bootcamps, and workforce programs:

* Convert missing skills into a weekly learning pathway
* Support students and career changers
* Create training plans based on real job descriptions
* Download a learning pathway report

---

## Target Careers

The app currently supports:

* AI Engineer
* Data Analyst
* Machine Learning Engineer
* AI Education Specialist

---

## Key Features

### PDF Resume Upload

Users can upload a PDF resume. The app extracts resume text and uses it for skill detection and job matching.

### Resume Skill Analyzer

Users can paste resume text or upload a PDF resume. The app detects skills such as:

* Python
* SQL
* Power BI
* Machine Learning
* Artificial Intelligence
* Data Analysis
* Communication

### Job Description Matching

Users can paste a job description. The app detects required job skills and compares them with the resume skills.

### Job Match Score

The app calculates how closely a resume matches a job description.

Example:

```text
Job Match Score: 50%
```

### Matched Skills

The app shows which skills appear in both the resume and the job description.

### Missing Skills

The app shows which job-required skills are missing from the resume.

### Personalized Course Plan

For each missing skill, the app generates a simple learning plan.

Example:

```text
Excel:
- Learn Excel formulas, tables, sorting, filtering, and pivot tables.
- Practice cleaning a messy spreadsheet dataset.
- Create one Excel dashboard and explain your findings.
```

### Portfolio Evidence Checklist

For job seekers, the app recommends portfolio evidence for missing skills.

Example:

```text
Build one small project that proves your ETL skill.
```

### HR Candidate Report

For HR / Recruiter Mode, the app generates a candidate report with:

* Candidate recommendation
* HR decision
* Job match score
* Candidate strengths
* Candidate skill gaps
* HR summary

Example:

```text
Candidate Recommendation: Train Before Interview
HR Decision: Recommend targeted training before final interview
```

### Training Center Learning Pathway

For Training Center Mode, the app turns missing skills into a weekly learning pathway.

Example:

```text
Week 1: Excel
Week 2: Statistics
Week 3: ETL
Week 4: Cloud
Week 5: Git
```

### Resume-Based Career Readiness

The app converts detected resume skills into estimated skill levels and compares them to the selected target career.

### Manual Skill Analyzer

Users can manually rate their skill levels using sliders.

### Downloadable Reports

The app supports downloadable text reports, including:

* Resume-based career report
* Manual career readiness report
* Full mode-based report for Job Seeker, HR / Recruiter, or Training Center Mode## New Version 2 Features

TalentBridge AI now includes advanced features that make it more than a resume scanner.

### Candidate Progress Tracker

TalentBridge AI turns missing skills into a progress tracker. For each missing skill, the app creates:

* A learning task
* A portfolio evidence requirement
* A progress status

Example:

```text
Missing Skill: ETL
Learning Task: Build a small ETL pipeline that extracts, cleans, transforms, and saves data.
Portfolio Evidence: Upload a GitHub link showing the ETL pipeline.
Status: Not Started
```

This helps job seekers prove improvement instead of only reading recommendations.

### Readiness Improvement Score

The app estimates how much a candidate’s readiness can improve after completing the recommended training path.

Example:

```text
Current Job Match Score: 50%
Estimated Score After Training: 80%
Improvement Potential: +30%
Status Change: Train Before Interview → Interview Ready
```

This helps job seekers, recruiters, and training centers understand the value of completing the learning plan.

### Recruiter and Job Seeker Feedback Loop

TalentBridge AI is designed to connect job seekers, recruiters, and training centers.

The product flow is:

```text
Resume + Job Description
↓
Skill Gap Analysis
↓
Personalized Course Plan
↓
Portfolio Evidence
↓
Progress Tracker
↓
Improved Candidate Readiness
↓
Recruiter-Ready Report
```

This makes the app different from simple resume scanners. Instead of only saying what is missing, TalentBridge AI shows the user how to become ready.
### Recruiter Feedback Report Download

In HR / Recruiter Mode, recruiters can enter candidate feedback, choose a decision, recommend next steps, and download a recruiter feedback report.

This supports a clear recruiter-to-candidate feedback workflow.

### Portfolio Evidence Links

In Job Seeker Mode, candidates can paste portfolio, GitHub, or project links for each missing skill.

This helps candidates prove that they are improving instead of only receiving recommendations.

### Candidate Progress Status

For every missing skill, candidates can mark progress as:

- Not Started
- In Progress
- Completed

This turns the app into a career progress tracker.

### Progress Completion Score

TalentBridge AI calculates how much of the missing-skill pathway the candidate has completed.

Example:

```text
Completed Skills: 2 of 5
Progress Completion Score: 40%
### Semantic Job-Resume Matching

TalentBridge AI now compares resumes and job descriptions in two ways:

- **Job Match Score**: compares detected skills from the resume and job description.
- **Semantic Match Score**: uses TF-IDF similarity to compare the meaning of the resume text and job description.

This helps identify candidates whose resume language may be different from the job posting but still has strong relevance.
### Proof-Based Readiness Score

TalentBridge AI goes beyond resume matching by measuring whether a candidate can prove their skills with real evidence.

The Proof-Based Readiness Score combines:

- Job Match Score
- Semantic Match Score
- Portfolio Evidence Score
- Progress Completion Score

This helps job seekers, recruiters, and training centers understand not only whether a resume matches a job, but whether the candidate has real proof of readiness through projects, GitHub links, dashboards, reports, or portfolio evidence.
### HR Batch Resume Screening

TalentBridge AI can compare one job description against multiple candidate resumes and rank candidates by readiness.

The HR Batch Screening feature provides:

- Job Match Score
- Semantic Match Score
- Final Screening Score
- Matched Skills
- Missing Skills
- Candidate Recommendation
- Downloadable HR screening report

This helps recruiters quickly identify strong candidates, candidates who need training, and candidates who are not ready yet.
### Candidate Interview Readiness Report

TalentBridge AI generates an interview readiness decision for the top-ranked candidate after HR batch screening.

The report includes:

- Interview Readiness Score
- Final Decision
- Missing Skills
- Plain-English Summary
- Recommended Next Step

This helps HR teams decide whether to interview, train, request portfolio evidence, or reject a candidate.
### Skill Confidence Scoring

TalentBridge AI does not only detect whether a skill appears in a resume. It also evaluates the strength of the evidence behind that skill.

The app classifies detected skills as:

- **Strong Evidence**: the resume shows practical use, such as built, created, used, analyzed, or developed.
- **Medium Evidence**: the resume suggests some project or experience exposure.
- **Weak Evidence**: the resume only says learning, beginner, interested in, or basic exposure.

This helps job seekers understand which skills are truly proven and which skills need stronger portfolio evidence.



### Dashboard-Style Layout

The app uses a tabbed dashboard layout:

* Resume & Job Match
* Career Readiness
* Product Vision

---

## Tools and Technologies

* Python
* Pandas
* Streamlit
* PyPDF2
* pathlib
* Rule-based AI logic
* Resume keyword extraction
* PDF text extraction
* Skill-gap analysis
* Job-description matching
* Career readiness scoring
* Report generation
* Git and GitHub
* Streamlit Cloud deployment

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
│   └── test_job_matcher.py
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
├── requirements.txt
├── .gitignore
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
c:\python314\python.exe -m pip install -r requirements.txt
```

If installing manually:

```powershell
c:\python314\python.exe -m pip install pandas streamlit PyPDF2
```

### 3. Test the backend

```powershell
cd C:\Users\nigus\OneDrive\Desktop\talentbridge-ai\backend
c:\python314\python.exe test_job_matcher.py
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
I am a Data Analyst with experience in Python, SQL, Power BI, data analysis, dashboards, data cleaning, communication, and machine learning basics.
```

---

## Sample Job Description for Testing

```text
We are hiring a Data Analyst. The candidate should have strong SQL, Python, Power BI, Excel, data visualization, statistics, ETL, and stakeholder communication skills. Experience with Git and cloud platforms is a plus.
```

---

## Example Output

For a Data Analyst job match, the app may show:

```text
Job Match Score: 50%

Matched Skills:
- Python
- SQL
- Power BI
- Data Analysis
- Communication

Missing Skills:
- Excel
- Statistics
- ETL
- Cloud
- Git
```

In Job Seeker Mode, the app generates a personalized course plan and portfolio checklist.

In HR / Recruiter Mode, the app generates an HR candidate report.

In Training Center Mode, the app generates a weekly learning pathway.

---

## What I Learned

Through this project, I practiced:

* Building a Python backend
* Creating reusable functions
* Reading and analyzing datasets
* Detecting skills from resume text
* Extracting text from PDF resumes
* Comparing resumes with job descriptions
* Creating a rule-based AI recommendation system
* Generating personalized course plans
* Generating HR-style candidate reports
* Building a Streamlit web app
* Creating a dashboard-style layout
* Debugging Python indentation and import errors
* Organizing a project for GitHub and portfolio use
* Deploying an app using Streamlit Cloud

---
## Business Case Tab

TalentBridge AI includes a Business Case tab that explains the product as a real AI career readiness platform.

### Problem

Many job seekers do not know why they are not getting interviews. Recruiters may see missing skills, but candidates often do not receive a clear path to improve. Training centers also need a way to connect learning programs to real job requirements.

### Solution

TalentBridge AI compares resumes with job descriptions, identifies matched and missing skills, creates personalized learning paths, tracks candidate progress, collects portfolio evidence, and generates recruiter-ready reports.

### Target Users

- Job seekers who want to become interview-ready
- HR teams and recruiters who need candidate-job fit reports
- Training centers that want to build job-aligned learning pathways

### Product Workflow

```text
Resume + Job Description
↓
Job Match Score
↓
Missing Skills
↓
Personalized Learning Path
↓
Portfolio Evidence Links
↓
Progress Status
↓
Completion Score
↓
Recruiter Feedback Report
↓
Improved Candidate Readiness
## Future Improvements

Planned improvements include:

* Add stronger NLP skill extraction
* Add machine learning model for career prediction
* Add semantic job-resume matching using embeddings
* Add RAG assistant for job and scholarship documents
* Add user login
* Add database storage
* Add HR batch resume screening
* Add training center dashboard
* Add progress tracking
* Add payment or subscription feature
* Add Power BI dashboard
* Improve UI design and branding

---

## Resume Bullet Point

Built TalentBridge AI, an end-to-end AI career readiness and training web application using Python and Streamlit. Developed backend logic to analyze resumes, extract PDF text, detect skills, compare resumes with job descriptions, calculate job match scores, identify skill gaps, generate personalized course plans, create HR-style candidate reports, and produce downloadable reports for job seekers, recruiters, and training centers.

---

## Project Status

Current version: Version 2.0
Status: Working Streamlit web app deployed online
Live Demo: https://talentbridge-ai-8e3fcvn6dzewqfbskts8dn.streamlit.app/
