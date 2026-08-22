# career_engine.py
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILL_KEYWORDS = {
    "Python": [
        "python", "python 3", "pandas", "numpy", "matplotlib",
        "seaborn", "jupyter", "google colab", "pytest",
    ],
    "SQL": [
        "sql", "sql server", "mysql", "postgresql", "postgres", "sqlite",
        "t sql", "pl sql", "relational database", "sql query", "sql queries",
    ],
    "Power BI": [
        "power bi", "powerbi", "microsoft power bi", "dax", "power query",
        "power pivot", "paginated report", "paginated reports",
    ],
    "Excel": [
        "excel", "ms excel", "microsoft excel", "pivot table", "pivot tables",
        "vlookup", "xlookup", "power pivot", "excel formulas", "spreadsheet",
        "spreadsheets", "google sheets",
    ],
    "Statistics": [
        "statistics", "statistical analysis", "probability",
        "hypothesis testing", "a b testing", "anova", "correlation",
        "standard deviation", "variance analysis", "regression analysis",
        "time series analysis",
    ],
    "ETL": [
        "etl", "elt", "extract transform load", "data pipeline",
        "data pipelines", "data transformation", "data integration",
        "data orchestration", "apache airflow", "airflow", "dbt",
        "azure data factory",
    ],
    "Git": [
        "git", "github", "gitlab", "bitbucket", "version control",
        "git repository", "git commit", "git push", "pull request",
        "pull requests",
    ],
    "Cloud": [
        "cloud", "cloud computing", "cloud platform", "cloud platforms",
        "cloud storage",
        "amazon web services", "aws", "microsoft azure", "azure",
        "google cloud platform", "google cloud", "gcp", "microsoft fabric",
    ],
    "Machine Learning": [
        "machine learning", "scikit learn", "sklearn", "tensorflow", "pytorch",
        "xgboost", "lightgbm", "model training", "predictive model",
        "predictive models", "supervised learning", "unsupervised learning",
        "random forest", "decision tree", "logistic regression",
        "neural network", "neural networks",
    ],
    "Artificial Intelligence": [
        "artificial intelligence", "generative ai", "genai",
        "large language model", "large language models", "llm", "llms",
        "retrieval augmented generation", "rag", "natural language processing",
        "nlp", "computer vision", "prompt engineering", "langchain", "openai",
        "ai model", "ai models", "ai system", "ai systems",
    ],
    "Data Analysis": [
        "data analysis", "data analytics", "analyze data",
        "analysed data", "analyzed data", "exploratory data analysis", "eda",
        "business insights", "trend analysis", "data profiling", "data cleaning",
    ],
    "Data Visualization": [
        "data visualization", "data visualisation", "visual analytics",
        "dashboard", "dashboards", "tableau", "plotly", "matplotlib", "seaborn",
    ],
    "Communication": [
        "communication", "written communication", "verbal communication",
        "presentation", "presentations", "presentation skills", "presented to",
        "stakeholder", "stakeholders", "stakeholder communication",
        "stakeholder management", "public speaking", "technical writing",
        "report writing", "teaching", "training",
    ],
    "FastAPI": ["fastapi"],
    "Streamlit": ["streamlit"],
    "REST APIs": [
        "rest api", "rest apis", "restful api", "restful apis",
        "api development",
    ],
    "Quality Assurance": [
        "quality assurance", "qa analyst", "qa testing", "data testing",
        "quality analyst", "software testing", "quality engineering",
    ],
    "Test Planning": [
        "test plan", "test plans", "test case", "test cases",
        "test script", "test scripts", "testing strategy",
    ],
    "Manual Testing": ["manual testing", "manual tester"],
    "Test Automation": [
        "test automation", "automated testing", "automation testing",
        "automated test", "automated tests",
    ],
    "Functional Testing": ["functional testing", "functional test"],
    "Regression Testing": [
        "regression testing", "regression test", "regression tests",
    ],
    "Integration Testing": [
        "integration testing", "integration test", "integration tests",
    ],
    "Performance Testing": [
        "performance testing", "performance test", "load testing",
        "stress testing",
    ],
    "System Testing": ["system testing", "system test", "system tests"],
    "User Acceptance Testing": [
        "user acceptance testing", "user acceptance test", "uat",
    ],
    "Defect Management": [
        "defect management", "defect tracking", "defect", "defects",
        "bug tracking", "bug fix", "bug fixes", "issue tracking",
    ],
    "Requirements Traceability": [
        "requirements traceability", "requirement traceability",
        "traceability of requirements", "traceability matrix",
        "requirements coverage",
    ],
    "Data Validation": [
        "data validation", "validate data", "validated data",
        "validation", "validate etl", "validated etl",
        "data reconciliation", "reconcile data", "reconciled data",
        "data quality", "data discrepancy", "data discrepancies",
    ],
    "ETL Testing": [
        "etl testing", "elt testing", "data pipeline testing",
        "pipeline testing", "source to target", "source target mapping",
        "source to target mapping", "data transformation testing",
    ],
    "API Testing": [
        "api testing", "api test", "api tests", "postman",
        "rest api testing", "restful api testing",
    ],
    "Pandas": ["pandas"],
    "PySpark": ["pyspark"],
    "Root Cause Analysis": [
        "root cause analysis", "root cause investigation",
    ],
    "Data Engineering": ["data engineering", "data engineer"],
    "Agile/Scrum": [
        "agile", "scrum", "sprint planning", "daily standup",
        "daily stand up",
    ],
    "Docker": [
        "docker", "dockerfile", "containerization", "containerisation",
    ],
    "Kubernetes": ["kubernetes", "k8s"],
    "Apache Spark": ["apache spark", "pyspark", "spark sql"],
    "Databricks": ["databricks"],
    "Linux": ["linux", "ubuntu", "bash scripting", "shell scripting"],
    "JavaScript": ["javascript", "typescript", "node.js", "nodejs"],
}


TESTING_CONTEXT_SKILLS = {
    "Manual Testing": ["manual"],
    "Test Automation": ["automated", "automation"],
    "Functional Testing": ["functional"],
    "Regression Testing": ["regression"],
    "Integration Testing": ["integration"],
    "Performance Testing": ["performance", "load", "stress"],
    "System Testing": ["system"],
}


def _normalize_skill_text(text):
    normalized = str(text or "").casefold()
    normalized = re.sub(r"[\u2010-\u2015/_-]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _contains_skill_keyword(normalized_text, keyword):
    normalized_keyword = _normalize_skill_text(keyword)
    pattern = rf"(?<![a-z0-9]){re.escape(normalized_keyword)}(?![a-z0-9])"
    return re.search(pattern, normalized_text) is not None


def _contains_data_analysis_action(normalized_text):
    pattern = (
        r"\banaly[sz](?:e|ed|ing)\b"
        r"(?:\s+[a-z0-9]+){0,4}\s+\b(?:data|datasets?)\b"
    )
    return re.search(pattern, normalized_text) is not None


def _contains_testing_mode(normalized_text, keyword):
    """Require a generic testing mode to occur in the same sentence as testing."""
    for sentence in re.split(r"[.;:]+", normalized_text):
        has_testing_marker = any(
            _contains_skill_keyword(sentence, marker)
            for marker in (
                "quality assurance",
                "qa analyst",
                "qa testing",
                "software testing",
                "data testing",
                "test plan",
                "test case",
                "test",
                "testing",
            )
        )
        if (
            has_testing_marker
            and _contains_skill_keyword(sentence, keyword)
        ):
            return True
    return False


def detect_skills(text):
    normalized_text = _normalize_skill_text(text)
    if not normalized_text:
        return []

    detected_skills = [
        skill
        for skill, keywords in SKILL_KEYWORDS.items()
        if any(
            _contains_skill_keyword(normalized_text, keyword)
            for keyword in keywords
        )
        or (
            skill in TESTING_CONTEXT_SKILLS
            and any(
                _contains_testing_mode(normalized_text, keyword)
                for keyword in TESTING_CONTEXT_SKILLS[skill]
            )
        )
    ]

    if (
        "Data Analysis" not in detected_skills
        and _contains_data_analysis_action(normalized_text)
    ):
        data_analysis_index = list(SKILL_KEYWORDS).index("Data Analysis")
        detected_skills.insert(data_analysis_index, "Data Analysis")

    return detected_skills

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
    },
    "QA Analyst / Data Quality Analyst": {
        "python_skill": 3,
        "math_skill": 2,
        "data_skill": 5,
        "ai_skill": 1,
        "communication_skill": 4
    }
}


QA_TARGET_CAREER = "QA Analyst / Data Quality Analyst"

CAREER_SKILL_BENCHMARKS = {
    QA_TARGET_CAREER: [
        "Quality Assurance",
        "Test Planning",
        "Data Validation",
        "ETL Testing",
        "Functional Testing",
        "Regression Testing",
        "Integration Testing",
        "User Acceptance Testing",
        "Defect Management",
        "SQL",
    ],
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

    for skill in gaps:
        recommended_projects[skill] = project_recommendations[skill]

    return {
        "target_career": target_career,
        "readiness_score": round(readiness_score, 2),
        "status": status,
        "skill_gaps": gaps,
        "recommended_projects": recommended_projects
    }

def analyze_resume_text(resume_text):
    return detect_skills(resume_text)

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


def calculate_target_career_match(detected_skills, target_career):
    """Score resume evidence against the selected career benchmark."""
    if target_career not in required_skills:
        raise ValueError(f"Unsupported target career: {target_career}")

    if not detected_skills:
        return {
            "target_career": target_career,
            "match_score": 0.0,
            "status": "No resume evidence detected",
            "skill_gaps": required_skills[target_career].copy(),
        }

    career_benchmark = CAREER_SKILL_BENCHMARKS.get(target_career)
    if career_benchmark:
        matched_skills = [
            skill for skill in career_benchmark if skill in detected_skills
        ]
        missing_skills = [
            skill for skill in career_benchmark if skill not in detected_skills
        ]
        match_score = round(
            (len(matched_skills) / len(career_benchmark)) * 100,
            2,
        )

        if match_score >= 90:
            status = "Strong candidate"
        elif match_score >= 75:
            status = "Almost ready"
        elif match_score >= 60:
            status = "Developing candidate"
        else:
            status = "Beginner level - build more foundation projects"

        return {
            "target_career": target_career,
            "match_score": match_score,
            "status": status,
            "skill_gaps": {skill: 1 for skill in missing_skills},
            "matched_skills": matched_skills,
        }

    estimated_profile = create_profile_from_resume(detected_skills)
    career_result = analyze_career_profile(estimated_profile, target_career)

    return {
        "target_career": target_career,
        "match_score": career_result["readiness_score"],
        "status": career_result["status"],
        "skill_gaps": career_result["skill_gaps"],
    }


def rank_career_matches(user_profile):
    """Rank every supported career using the existing readiness model."""
    rankings = []

    for career_name in required_skills:
        career_result = analyze_career_profile(user_profile, career_name)
        target_requirements = required_skills[career_name]
        strengths = [
            skill
            for skill, required_level in target_requirements.items()
            if user_profile.get(skill, 0) >= required_level
        ]

        rankings.append(
            {
                "career": career_name,
                "fit_score": career_result["readiness_score"],
                "status": career_result["status"],
                "strengths": strengths,
                "skill_gaps": career_result["skill_gaps"],
            }
        )

    rankings.sort(key=lambda item: item["fit_score"], reverse=True)

    for rank, item in enumerate(rankings, start=1):
        item["rank"] = rank

    return rankings


def recommend_careers_from_resume(resume_text):
    """Create an explainable career ranking from detected resume evidence."""
    detected_skills = analyze_resume_text(resume_text)

    if not detected_skills:
        return {
            "recommended_career": None,
            "recommended_score": 0.0,
            "detected_skills": [],
            "estimated_profile": None,
            "rankings": [],
        }

    estimated_profile = create_profile_from_resume(detected_skills)
    rankings = rank_career_matches(estimated_profile)
    best_match = rankings[0]

    return {
        "recommended_career": best_match["career"],
        "recommended_score": best_match["fit_score"],
        "detected_skills": detected_skills,
        "estimated_profile": estimated_profile,
        "rankings": rankings,
    }


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
    return detect_skills(job_description_text)


ANALYSIS_INSTRUCTION_PHRASES = (
    "click compare",
    "compare resume to job description",
    "send me a screenshot",
    "reboot app",
    "manage app",
    "tell me qa career appears",
)


CRITICAL_TECHNOLOGY_SKILLS = (
    "Python",
    "SQL",
    "Power BI",
    "Excel",
    "ETL",
    "Cloud",
    "Machine Learning",
    "FastAPI",
    "REST APIs",
    "API Testing",
    "Pandas",
    "PySpark",
    "Docker",
    "Kubernetes",
    "Apache Spark",
    "Databricks",
    "Linux",
    "JavaScript",
)


CERTIFICATION_PATTERNS = {
    "ISTQB certification": r"\bistqb\b",
    "CSTE certification": r"\bcste\b",
    "CSQA certification": r"\bcsqa\b",
    "PMP certification": r"\bpmp\b",
    "CISSP certification": r"\bcissp\b",
    "Security+ certification": r"\bsecurity\s*\+\b",
    "AWS certification": r"\baws\s+certif(?:ied|ication)\b",
    "Azure certification": r"\bazure\s+certif(?:ied|ication)\b",
}


EDUCATION_LEVELS = {
    "High school diploma": (1, r"\b(?:high school diploma|ged)\b"),
    "Associate degree": (
        2,
        r"\b(?:associate(?:'s)?\s+degree|associate\s+of\s+(?:science|arts))\b",
    ),
    "Bachelor's degree": (
        3,
        r"\b(?:bachelor(?:'s)?\s+degree|bachelor\s+of\s+(?:science|arts))\b",
    ),
    "Master's degree": (
        4,
        r"\b(?:master(?:'s)?\s+degree|master\s+of\s+(?:science|arts))\b",
    ),
    "Doctoral degree": (5, r"\b(?:doctoral degree|doctorate|ph\.?d\.?)\b"),
}


def _requirement_sentences(text):
    """Split prose and numbered lists into compact requirement statements."""
    return [
        sentence.strip(" -\t")
        for sentence in re.split(r"(?<=[.!?])\s+|[\r\n]+", str(text or ""))
        if sentence.strip(" -\t")
    ]


def _is_optional_requirement(text):
    return re.search(
        r"\b(?:preferred|nice to have|bonus|desirable|optional)\b",
        _normalize_skill_text(text),
    ) is not None


def _experience_years(text):
    return [
        int(match.group("years"))
        for match in re.finditer(
            r"(?P<years>\d{1,2})\s*\+?\s*(?:years?|yrs?)\s+"
            r"(?:of\s+)?experience",
            _normalize_skill_text(text),
        )
    ]


def _highest_education_level(text):
    normalized_text = _normalize_skill_text(text)
    matches = [
        (level, label)
        for label, (level, pattern) in EDUCATION_LEVELS.items()
        if re.search(pattern, normalized_text)
    ]
    return max(matches, default=(0, None))


def _required_education_level(text):
    matches = []
    for sentence in _requirement_sentences(text):
        if _is_optional_requirement(sentence):
            continue
        level, label = _highest_education_level(sentence)
        if label:
            matches.append((level, label))
    return max(matches, default=(0, None))


def _seniority_level(text):
    normalized_text = _normalize_skill_text(text)
    seniority_patterns = (
        (
            4,
            "Principal",
            r"\bprincipal(?:\s+level)?\s+(?:engineer|analyst|scientist|"
            r"developer|architect|consultant|role|candidate)\b",
        ),
        (
            3,
            "Senior",
            r"\bsenior(?:\s+level)?(?:\s+(?:engineer|analyst|scientist|"
            r"developer|architect|consultant|role|candidate))?\b",
        ),
        (2, "Mid-level", r"\b(?:mid\s+level|intermediate)\b"),
        (1, "Entry-level", r"\b(?:entry\s+level|junior)\b"),
    )
    for level, label, pattern in seniority_patterns:
        if re.search(pattern, normalized_text):
            return level, label
    return 0, None


def _critical_job_technology_skills(job_description_text):
    explicit_skills = set()
    requirement_markers = re.compile(
        r"\b(?:required|must|minimum|strong|advanced|hands on|proficien\w*|"
        r"experience\s+(?:with|using|testing|designing|developing)|skills?)\b"
    )

    for sentence in _requirement_sentences(job_description_text):
        normalized_sentence = _normalize_skill_text(sentence)
        if (
            _is_optional_requirement(sentence)
            or requirement_markers.search(normalized_sentence) is None
        ):
            continue
        explicit_skills.update(detect_skills(sentence))

    return explicit_skills


def evaluate_critical_requirements(resume_text, job_description_text):
    """Compare explicit non-score job requirements with résumé evidence.

    The result intentionally uses ``Unclear`` whenever the text does not prove
    a claim. This keeps the check useful without inventing experience.
    """
    resume_text = str(resume_text or "").strip()
    job_description_text = str(job_description_text or "").strip()
    normalized_resume = _normalize_skill_text(resume_text)
    resume_skills = set(detect_skills(resume_text))
    job_skills = set(detect_skills(job_description_text))
    critical_job_skills = _critical_job_technology_skills(job_description_text)
    resume_years = _experience_years(resume_text)
    requirements = []

    job_level, job_level_label = _seniority_level(job_description_text)
    resume_level, resume_level_label = _seniority_level(resume_text)
    if job_level_label:
        if resume_level >= job_level:
            status = "Met"
            evidence = f"Résumé explicitly indicates {resume_level_label} level."
        elif resume_level:
            status = "Missing"
            evidence = (
                f"Résumé indicates {resume_level_label} level, below the stated "
                f"{job_level_label} level."
            )
        else:
            status = "Unclear"
            evidence = "No explicit seniority level was found in the résumé."
        requirements.append(
            {
                "category": "Seniority",
                "requirement": f"{job_level_label}-level candidate",
                "status": status,
                "evidence": evidence,
            }
        )

    experience_pattern = re.compile(
        r"(?P<years>\d{1,2})\s*\+?\s*(?:years?|yrs?)\s+"
        r"(?:of\s+)?experience",
        re.IGNORECASE,
    )
    for sentence in _requirement_sentences(job_description_text):
        if _is_optional_requirement(sentence):
            continue
        for match in experience_pattern.finditer(sentence):
            required_years = int(match.group("years"))
            related_skills = [
                skill for skill in detect_skills(sentence) if skill in job_skills
            ]
            missing_related_skills = [
                skill for skill in related_skills if skill not in resume_skills
            ]
            leadership_required = re.search(
                r"\b(?:lead|leading|leadership|manage|managing)\b",
                _normalize_skill_text(sentence),
            ) is not None
            leadership_evidence = re.search(
                r"\b(?:led|lead|leading|managed|manager|supervised|oversaw|directed)\b",
                normalized_resume,
            ) is not None

            if not resume_years:
                status = "Unclear"
                evidence = "The résumé does not state a total number of experience years."
            elif max(resume_years) < required_years:
                status = "Missing"
                evidence = (
                    f"Résumé states up to {max(resume_years)} years; the job "
                    f"requires {required_years}+ years."
                )
            elif leadership_required and not leadership_evidence:
                status = "Unclear"
                evidence = (
                    f"Résumé states {max(resume_years)}+ years, but leadership "
                    "duration is not explicit."
                )
            elif missing_related_skills:
                status = "Unclear"
                evidence = (
                    f"Résumé states {max(resume_years)}+ years, but the duration "
                    "is not clearly tied to: "
                    + ", ".join(missing_related_skills[:3])
                    + "."
                )
            else:
                status = "Met"
                evidence = (
                    f"Résumé explicitly states {max(resume_years)}+ years of "
                    "experience."
                )

            requirement_label = f"{required_years}+ years of experience"
            if leadership_required:
                requirement_label += " in a leadership capacity"
            elif related_skills:
                requirement_label += " with " + ", ".join(related_skills[:3])
            requirements.append(
                {
                    "category": "Experience",
                    "requirement": requirement_label,
                    "status": status,
                    "evidence": evidence,
                }
            )

    job_education_level, job_education_label = _required_education_level(
        job_description_text
    )
    resume_education_level, resume_education_label = _highest_education_level(
        resume_text
    )
    if job_education_label:
        if resume_education_level >= job_education_level:
            status = "Met"
            evidence = f"Résumé lists {resume_education_label}."
        elif resume_education_level:
            status = "Missing"
            evidence = (
                f"Résumé lists {resume_education_label}, below the stated "
                f"{job_education_label}."
            )
        else:
            status = "Unclear"
            evidence = "No degree level was detected in the résumé text."
        requirements.append(
            {
                "category": "Education",
                "requirement": job_education_label,
                "status": status,
                "evidence": evidence,
            }
        )

    certification_found = False
    for certification_label, pattern in CERTIFICATION_PATTERNS.items():
        certification_required = any(
            re.search(pattern, _normalize_skill_text(sentence))
            and not _is_optional_requirement(sentence)
            for sentence in _requirement_sentences(job_description_text)
        )
        if certification_required:
            certification_found = True
            certification_met = re.search(pattern, normalized_resume) is not None
            requirements.append(
                {
                    "category": "Certification",
                    "requirement": certification_label,
                    "status": "Met" if certification_met else "Missing",
                    "evidence": (
                        "Exact certification name detected in the résumé."
                        if certification_met
                        else "Exact certification name not detected in the résumé."
                    ),
                }
            )

    generic_certification_required = any(
        re.search(
            r"\b(?:certification|certified|professional license)\b",
            _normalize_skill_text(sentence),
        )
        and not _is_optional_requirement(sentence)
        for sentence in _requirement_sentences(job_description_text)
    )
    if not certification_found and generic_certification_required:
        requirements.append(
            {
                "category": "Certification",
                "requirement": "Job-specific certification or license",
                "status": "Unclear",
                "evidence": (
                    "The posting mentions certification, but the exact credential "
                    "could not be compared automatically."
                ),
            }
        )

    for skill in CRITICAL_TECHNOLOGY_SKILLS:
        if skill not in critical_job_skills:
            continue
        skill_met = skill in resume_skills
        requirements.append(
            {
                "category": "Technology",
                "requirement": skill,
                "status": "Met" if skill_met else "Missing",
                "evidence": (
                    "Skill detected in the résumé text."
                    if skill_met
                    else "Skill not detected in the résumé text."
                ),
            }
        )

    status_counts = {
        status: sum(
            requirement["status"] == status for requirement in requirements
        )
        for status in ("Met", "Unclear", "Missing")
    }
    if status_counts["Missing"]:
        overall_status = "Critical gaps detected"
    elif status_counts["Unclear"]:
        overall_status = "Evidence needs verification"
    elif requirements:
        overall_status = "Critical requirements supported"
    else:
        overall_status = "No explicit critical requirements detected"

    return {
        "requirements": requirements,
        "met_count": status_counts["Met"],
        "unclear_count": status_counts["Unclear"],
        "missing_count": status_counts["Missing"],
        "overall_status": overall_status,
        "disclaimer": (
            "This evidence check uses only the pasted text. Unclear items require "
            "human verification and should never be treated as proven."
        ),
    }


def validate_analysis_inputs(resume_text, job_description_text):
    """Assess whether the two inputs are suitable for a meaningful analysis."""
    resume_text = str(resume_text or "").strip()
    job_description_text = str(job_description_text or "").strip()
    resume_word_count = len(re.findall(r"\b\w+\b", resume_text))
    job_word_count = len(re.findall(r"\b\w+\b", job_description_text))
    detected_resume_skills = detect_skills(resume_text)
    detected_job_skills = detect_skills(job_description_text)
    normalized_job_text = _normalize_skill_text(job_description_text)

    errors = []
    warnings = []

    if resume_word_count < 3:
        errors.append(
            "The resume input is too short. Add skills, projects, or work "
            "experience before analyzing."
        )

    if job_word_count < 5:
        errors.append(
            "The job description is too short. Paste the responsibilities and "
            "required qualifications before analyzing."
        )

    instruction_phrases = [
        phrase
        for phrase in ANALYSIS_INSTRUCTION_PHRASES
        if phrase in normalized_job_text
    ]
    if instruction_phrases:
        errors.append(
            "The Job Description box appears to contain app or chat "
            "instructions. Replace them with the actual job posting."
        )

    if 0 < resume_word_count < 40:
        warnings.append(
            "The resume text is brief, so some skills or evidence may be missed."
        )

    if 0 < job_word_count < 50:
        warnings.append(
            "The job description is brief, so the match score may be incomplete."
        )

    if job_word_count >= 5 and len(detected_job_skills) < 3:
        warnings.append(
            "Fewer than three recognizable job skills were detected. Confirm "
            "that the complete job requirements were pasted."
        )

    if errors:
        quality_level = "Blocked"
    elif warnings:
        quality_level = "Review Recommended"
    else:
        quality_level = "Ready"

    return {
        "can_analyze": not errors,
        "quality_level": quality_level,
        "resume_word_count": resume_word_count,
        "job_word_count": job_word_count,
        "resume_skill_count": len(detected_resume_skills),
        "job_skill_count": len(detected_job_skills),
        "errors": errors,
        "warnings": warnings,
    }


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
def calculate_improvement_score(job_comparison):
    current_score = job_comparison["match_score"]
    matched_skills = job_comparison.get("matched_skills", [])
    missing_skills = job_comparison["missing_skills"]
    total_required_skills = len(matched_skills) + len(missing_skills)

    # This is a planning scenario, not a promise. Assume the candidate closes
    # and proves roughly half of the current gaps, then cap the projection below
    # 100 while any gaps remain. A perfect score is reserved for evidence that
    # already matches every detected requirement.
    projected_gap_closures = (len(missing_skills) + 1) // 2
    if total_required_skills == 0:
        estimated_score = current_score
    elif not missing_skills:
        estimated_score = 100.0
    else:
        estimated_score = (
            (len(matched_skills) + projected_gap_closures)
            / total_required_skills
        ) * 100
        estimated_score = min(estimated_score, 95.0)

    estimated_score = max(current_score, estimated_score)

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
        "estimated_status_after_training": estimated_status,
        "projected_gap_closures": projected_gap_closures,
        "total_missing_skills": len(missing_skills),
        "projection_assumption": (
            "Planning estimate only: assumes the candidate completes and "
            f"proves {projected_gap_closures} of {len(missing_skills)} current "
            "skill gaps. It is not a guaranteed result."
        ),
    }
def prioritize_missing_skills(missing_skills, target_career=None):
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
        "Data Analysis",
        "Data Engineering",
        "Agile/Scrum"
    ]

    qa_high_priority = {
        "Quality Assurance",
        "Test Planning",
        "Manual Testing",
        "Test Automation",
        "Functional Testing",
        "Regression Testing",
        "Integration Testing",
        "Performance Testing",
        "System Testing",
        "User Acceptance Testing",
        "Defect Management",
        "Requirements Traceability",
        "Data Validation",
        "ETL Testing",
        "API Testing",
        "REST APIs",
        "Apache Spark",
        "PySpark",
        "Databricks",
        "Pandas",
        "Root Cause Analysis",
    }

    priority_report = []

    for skill in missing_skills:
        if target_career == QA_TARGET_CAREER and skill in qa_high_priority:
            priority = "High Priority"
        elif skill in high_priority:
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


def generate_match_action_summary(job_comparison, target_career=None):
    """Turn match evidence into a concise, non-hiring action summary."""
    matched_skills = job_comparison.get("matched_skills", [])
    missing_skills = job_comparison.get("missing_skills", [])
    match_score = float(job_comparison.get("match_score", 0) or 0)
    requirement_count = len(matched_skills) + len(missing_skills)

    if requirement_count == 0:
        return {
            "fit_level": "Insufficient Job Information",
            "message_type": "warning",
            "headline": "No recognizable job requirements were detected.",
            "top_strengths": [],
            "priority_gaps": [],
            "next_action": (
                "Paste a detailed job description containing responsibilities "
                "and required skills, then run the comparison again."
            ),
            "disclaimer": "This summary is guidance, not a hiring decision.",
        }

    if match_score >= 80:
        fit_level = "Strong Skill Match"
        message_type = "success"
    elif match_score >= 65:
        fit_level = "Competitive Skill Match"
        message_type = "info"
    elif match_score >= 50:
        fit_level = "Developing Skill Match"
        message_type = "warning"
    else:
        fit_level = "Low Skill Match"
        message_type = "warning"

    priority_rank = {
        "High Priority": 0,
        "Medium Priority": 1,
        "Low Priority": 2,
    }
    priority_report = prioritize_missing_skills(
        missing_skills,
        target_career=target_career,
    )
    ranked_gaps = sorted(
        enumerate(priority_report),
        key=lambda item: (
            priority_rank.get(item[1]["Priority Level"], 3),
            item[0],
        ),
    )
    priority_gaps = [
        item["Missing Skill"] for _, item in ranked_gaps[:3]
    ]

    if priority_gaps:
        gap_text = ", ".join(priority_gaps)
        next_action = (
            f"Focus first on {gap_text}. Add a skill to the resume only after "
            "you can support it with truthful evidence."
        )
    else:
        next_action = (
            "Prepare evidence-based interview stories for the strongest matched "
            "skills and verify that every claim is accurate."
        )

    return {
        "fit_level": fit_level,
        "message_type": message_type,
        "headline": (
            f"{fit_level}: matched {len(matched_skills)} of "
            f"{requirement_count} detected job requirements."
        ),
        "top_strengths": matched_skills[:3],
        "priority_gaps": priority_gaps,
        "next_action": next_action,
        "disclaimer": "This summary is guidance, not a hiring decision.",
    }


def generate_application_decision(
    job_comparison,
    semantic_match_score,
    critical_requirements,
):
    """Create a cautious application recommendation from existing evidence."""
    matched_skills = job_comparison.get("matched_skills", [])
    missing_skills = job_comparison.get("missing_skills", [])
    skill_match_score = float(job_comparison.get("match_score", 0) or 0)
    semantic_match_score = float(semantic_match_score or 0)
    requirement_count = len(matched_skills) + len(missing_skills)

    critical_requirements = critical_requirements or {}
    critical_items = critical_requirements.get("requirements", [])
    met_count = int(critical_requirements.get("met_count", 0) or 0)
    unclear_count = int(critical_requirements.get("unclear_count", 0) or 0)
    missing_count = int(critical_requirements.get("missing_count", 0) or 0)
    critical_count = met_count + unclear_count + missing_count
    critical_support_score = None
    if critical_count:
        critical_support_score = round(
            ((met_count + (0.5 * unclear_count)) / critical_count) * 100,
            2,
        )

    blocking_categories = {
        "Seniority",
        "Experience",
        "Education",
        "Certification",
    }
    blocking_requirements = [
        item["requirement"]
        for item in critical_items
        if item.get("status") == "Missing"
        and item.get("category") in blocking_categories
    ]

    reasons = []
    if requirement_count:
        reasons.append(
            f"Skill evidence: matched {len(matched_skills)} of "
            f"{requirement_count} detected job requirements "
            f"({round(skill_match_score, 2)}%)."
        )
    reasons.append(
        f"Context alignment: semantic match is "
        f"{round(semantic_match_score, 2)}%."
    )
    if critical_count:
        reasons.append(
            "Critical evidence: "
            f"{met_count} met, {unclear_count} unclear, {missing_count} missing."
        )

    if requirement_count == 0:
        decision = "Insufficient Information"
        message_type = "warning"
        headline = "More job information is needed before making a recommendation."
        next_action = (
            "Paste the complete responsibilities and required qualifications, "
            "then run the analysis again."
        )
    elif (
        blocking_requirements
        or skill_match_score < 50
        or (
            critical_support_score is not None
            and critical_support_score < 50
        )
        or (skill_match_score < 65 and semantic_match_score < 30)
    ):
        decision = "Improve Before Applying"
        message_type = "warning"
        headline = (
            "Important evidence gaps should be addressed before treating this "
            "as a strong match."
        )
        if blocking_requirements:
            next_action = (
                "Verify or truthfully address: "
                + ", ".join(blocking_requirements[:3])
                + ". Do not claim evidence that the résumé cannot support."
            )
        elif missing_skills:
            next_action = (
                "Start with the highest-priority missing skills: "
                + ", ".join(missing_skills[:3])
                + ". Add them only after you can prove them truthfully."
            )
        else:
            next_action = (
                "Strengthen the résumé with truthful evidence that directly "
                "matches the responsibilities in the posting."
            )
    elif (
        skill_match_score >= 80
        and semantic_match_score >= 60
        and missing_count == 0
        and unclear_count <= 1
    ):
        decision = "Strong Match"
        message_type = "success"
        headline = (
            "The available résumé evidence strongly supports this job match."
        )
        next_action = (
            "Tailor the résumé to the posting and prepare evidence-based "
            "interview examples for the strongest requirements."
        )
    else:
        decision = "Consider Applying"
        message_type = "info"
        headline = (
            "The role shows useful alignment, with gaps that need review."
        )
        if unclear_count or missing_count:
            next_action = (
                "Review every unclear or missing critical requirement, then "
                "tailor the résumé using only evidence you can explain and prove."
            )
        else:
            next_action = (
                "Tailor the résumé to the posting and prepare truthful examples "
                "for the matched skills."
            )

    return {
        "decision": decision,
        "message_type": message_type,
        "headline": headline,
        "reasons": reasons,
        "next_action": next_action,
        "critical_support_score": critical_support_score,
        "blocking_requirements": blocking_requirements,
        "disclaimer": (
            "This is evidence-based guidance, not an employer decision, "
            "eligibility ruling, or guarantee of an interview."
        ),
    }


SEMANTIC_CONTEXT_WEIGHT = 0.35
SEMANTIC_SKILL_WEIGHT = 0.65


def _prepare_semantic_text(text):
    """Normalize text and append canonical skill concepts for comparison."""
    normalized_text = _normalize_skill_text(text)
    canonical_skills = " ".join(
        _normalize_skill_text(skill) for skill in detect_skills(text)
    )
    return " ".join(part for part in (normalized_text, canonical_skills) if part)


def _calculate_context_similarity(resume_text, job_description_text):
    texts = [
        _prepare_semantic_text(resume_text),
        _prepare_semantic_text(job_description_text),
    ]

    if not all(texts):
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True,
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
    except ValueError:
        # Both inputs can contain only punctuation or English stop words.
        return 0.0

    similarity_score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2],
    )[0][0]
    return round(float(similarity_score) * 100, 2)


def calculate_semantic_match_details(resume_text, job_description_text):
    """Return an explainable context-and-skill relevance score."""
    context_similarity_score = _calculate_context_similarity(
        resume_text,
        job_description_text,
    )
    resume_skills = detect_skills(resume_text)
    job_required_skills = detect_skills(job_description_text)
    matched_required_skills = [
        skill for skill in job_required_skills if skill in resume_skills
    ]

    if job_required_skills:
        skill_alignment_score = round(
            (len(matched_required_skills) / len(job_required_skills)) * 100,
            2,
        )
        semantic_score = round(
            (context_similarity_score * SEMANTIC_CONTEXT_WEIGHT)
            + (skill_alignment_score * SEMANTIC_SKILL_WEIGHT),
            2,
        )
        scoring_method = "context_and_required_skills"
    else:
        skill_alignment_score = 0.0
        semantic_score = context_similarity_score
        scoring_method = "context_only"

    return {
        "semantic_score": semantic_score,
        "context_similarity_score": context_similarity_score,
        "skill_alignment_score": skill_alignment_score,
        "matched_required_skills": matched_required_skills,
        "matched_required_skill_count": len(matched_required_skills),
        "required_skill_count": len(job_required_skills),
        "scoring_method": scoring_method,
    }


def calculate_semantic_match_score(resume_text, job_description_text):
    return calculate_semantic_match_details(
        resume_text,
        job_description_text,
    )["semantic_score"]


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

        skill_confidence_report = analyze_skill_confidence(
            resume_text,
            resume_skills
        )

        strong_skills = []
        weak_skills = []

        matched_skills = job_comparison["matched_skills"]

        for skill_item in skill_confidence_report:
            skill_name = skill_item["Skill"]

            if skill_name in matched_skills:
                if skill_item["Confidence Level"] == "Strong Evidence":
                    strong_skills.append(skill_name)
                elif skill_item["Confidence Level"] == "Weak Evidence":
                    weak_skills.append(skill_name)

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
                "Job Match Score": round(job_comparison["match_score"], 2),
                "Semantic Match Score": round(semantic_score, 2),
                "Final Screening Score": round(final_screening_score, 2),
                "Matched Skills": ", ".join(job_comparison["matched_skills"]),
                "Missing Skills": ", ".join(job_comparison["missing_skills"]),
                "Strong Evidence Skills": ", ".join(strong_skills),
                "Weak Evidence Skills": ", ".join(weak_skills),
                "Recommendation": recommendation
            }
        )

    screening_results = sorted(
        screening_results,
        key=lambda x: x["Final Screening Score"],
        reverse=True
    )

    return screening_results


def generate_interview_readiness_report(
    candidate_name,
    job_match_score,
    semantic_match_score,
    missing_skills,
    proof_based_score=None
):
    if proof_based_score is None:
        final_score = round(
            (job_match_score * 0.60) + (semantic_match_score * 0.40),
            2
        )
    else:
        final_score = round(
            (job_match_score * 0.35)
            + (semantic_match_score * 0.25)
            + (proof_based_score * 0.40),
            2
        )

    if final_score >= 85 and len(missing_skills) <= 1:
        decision = "Interview Ready"
    elif final_score >= 70:
        decision = "Needs Portfolio Evidence"
    elif final_score >= 50:
        decision = "Train Before Interview"
    else:
        decision = "Not Ready Yet"

    if len(missing_skills) == 0:
        missing_skills_text = "No major missing skills detected."
    else:
        missing_skills_text = ", ".join(missing_skills)

    summary = (
        f"{candidate_name} received a final interview readiness score of "
        f"{final_score}%. The current decision is: {decision}. "
        f"Missing skills: {missing_skills_text}"
    )

    if decision == "Interview Ready":
        next_step = "Move the candidate to interview."
    elif decision == "Needs Portfolio Evidence":
        next_step = "Ask the candidate to provide stronger GitHub, dashboard, or portfolio evidence."
    elif decision == "Train Before Interview":
        next_step = "Recommend a short training plan before interview."
    else:
        next_step = "Do not move forward yet. Candidate needs major skill development."

    return {
        "candidate_name": candidate_name,
        "final_score": final_score,
        "decision": decision,
        "missing_skills": missing_skills_text,
        "summary": summary,
        "next_step": next_step
    }
def analyze_skill_confidence(resume_text, detected_skills):
    resume_text_lower = _normalize_skill_text(resume_text)

    strong_evidence_words = [
        "built",
        "created",
        "developed",
        "implemented",
        "designed",
        "used",
        "applied",
        "analyzed",
        "cleaned",
        "automated",
        "deployed",
        "managed",
        "wrote",
        "generated",
        "presented",
        "transformed",
        "loaded",
        "extracted",
        "documented"
    ]

    medium_evidence_words = [
        "experience",
        "worked with",
        "hands-on",
        "project",
        "projects",
        "portfolio",
        "practice",
        "familiar",
        "completed",
        "support",
        "exposure"
    ]

    weak_evidence_words = [
        "learning",
        "currently learning",
        "interested",
        "beginner",
        "basic",
        "studying",
        "exploring",
        "introduced to",
        "currently improving",
        "practicing"
    ]

    sentences = re.split(r"[.!?\n]+", resume_text_lower)

    confidence_results = []

    for skill in detected_skills:
        skill_keywords = SKILL_KEYWORDS.get(skill, [skill])
        matching_sentences = [
            sentence
            for sentence in sentences
            if any(
                _contains_skill_keyword(sentence, keyword)
                for keyword in skill_keywords
            )
            or (
                skill == "Data Analysis"
                and _contains_data_analysis_action(sentence)
            )
        ]

        if len(matching_sentences) == 0:
            confidence = "Weak Evidence"
            reason = "Skill detected indirectly, but no direct resume sentence proves it."
        else:
            has_strong_evidence = False
            has_medium_evidence = False
            has_weak_evidence = False

            for sentence in matching_sentences:
                if any(word in sentence for word in strong_evidence_words):
                    has_strong_evidence = True

                if any(word in sentence for word in medium_evidence_words):
                    has_medium_evidence = True

                if any(word in sentence for word in weak_evidence_words):
                    has_weak_evidence = True

            if has_strong_evidence:
                confidence = "Strong Evidence"
                reason = "Resume includes action words showing practical use of this skill."
            elif has_medium_evidence:
                confidence = "Medium Evidence"
                reason = "Resume suggests project, portfolio, or experience exposure."
            elif has_weak_evidence:
                confidence = "Weak Evidence"
                reason = "Resume suggests learning or beginner-level exposure."
            else:
                confidence = "Medium Evidence"
                reason = "Skill is mentioned, but evidence strength is unclear."

        confidence_results.append(
            {
                "Skill": skill,
                "Confidence Level": confidence,
                "Reason": reason
            }
        )

    return confidence_results


def generate_resume_improvement_plan(resume_text, job_required_skills):
    """Create truthful, job-specific resume improvement guidance."""
    required_skills = list(dict.fromkeys(job_required_skills or []))

    if not required_skills:
        return {
            "required_skill_count": 0,
            "matched_skill_count": 0,
            "missing_skill_count": 0,
            "needs_stronger_evidence_count": 0,
            "strong_evidence_count": 0,
            "status": "No job requirements detected.",
            "actions": [],
            "truthfulness_note": (
                "Never invent skills, experience, projects, or measurable results."
            ),
        }

    detected_skills = analyze_resume_text(resume_text)
    comparison = compare_resume_to_job(detected_skills, required_skills)
    confidence_report = analyze_skill_confidence(resume_text, detected_skills)
    confidence_by_skill = {
        item["Skill"]: item["Confidence Level"]
        for item in confidence_report
    }

    actions = []
    strong_evidence_count = 0
    needs_stronger_evidence_count = 0
    missing_skills = set(comparison["missing_skills"])

    for skill in required_skills:
        bullet_prompt = (
            f"[Action verb] [task or project] using {skill}, resulting in "
            "[truthful measurable outcome]."
        )

        if skill in missing_skills:
            priority = "High"
            evidence_level = "Missing"
            guidance = (
                "Do not add this skill unless it is truthful. First complete or "
                "document a real project, course, or work example."
            )
        else:
            evidence_level = confidence_by_skill.get(skill, "Weak Evidence")

            if evidence_level == "Strong Evidence":
                priority = "Maintain"
                strong_evidence_count += 1
                guidance = (
                    "Keep the existing evidence. Add scale, scope, or a measurable "
                    "outcome if that information is available."
                )
            elif evidence_level == "Medium Evidence":
                priority = "Medium"
                needs_stronger_evidence_count += 1
                guidance = (
                    "Strengthen the mention with a truthful action, project context, "
                    "and measurable outcome."
                )
            else:
                priority = "Medium"
                needs_stronger_evidence_count += 1
                guidance = (
                    "Replace learning-only language with completed evidence only "
                    "after you have genuinely used the skill."
                )

        actions.append(
            {
                "Priority": priority,
                "Skill": skill,
                "Current Evidence": evidence_level,
                "Guidance": guidance,
                "Truthful Bullet Prompt": bullet_prompt,
            }
        )

    priority_order = {"High": 0, "Medium": 1, "Maintain": 2}
    actions.sort(key=lambda item: priority_order[item["Priority"]])

    missing_skill_count = len(comparison["missing_skills"])
    if missing_skill_count:
        status = (
            f"Close or honestly document {missing_skill_count} missing required "
            "skill(s) before presenting this resume as a complete match."
        )
    elif needs_stronger_evidence_count:
        status = (
            f"All required skills are mentioned, but {needs_stronger_evidence_count} "
            "skill(s) need stronger evidence."
        )
    else:
        status = (
            "All detected job requirements have strong resume evidence. Focus on "
            "clarity, measurable outcomes, and concise tailoring."
        )

    return {
        "required_skill_count": len(required_skills),
        "matched_skill_count": len(comparison["matched_skills"]),
        "missing_skill_count": missing_skill_count,
        "needs_stronger_evidence_count": needs_stronger_evidence_count,
        "strong_evidence_count": strong_evidence_count,
        "status": status,
        "actions": actions,
        "truthfulness_note": (
            "Never invent skills, experience, projects, or measurable results. "
            "Use each bullet prompt only with facts you can explain and prove."
        ),
    }


def generate_interview_preparation_plan(resume_text, job_required_skills):
    """Create truthful interview practice from the resume and job requirements."""
    required_skills = list(dict.fromkeys(job_required_skills or []))

    if not required_skills:
        return {
            "required_skill_count": 0,
            "technical_question_count": 0,
            "behavioral_question_count": 0,
            "high_priority_question_count": 0,
            "missing_skill_count": 0,
            "status": "No job requirements detected.",
            "technical_questions": [],
            "behavioral_questions": [],
            "truthfulness_note": (
                "Never invent interview answers, experience, projects, or results."
            ),
        }

    detected_skills = analyze_resume_text(resume_text)
    comparison = compare_resume_to_job(detected_skills, required_skills)
    confidence_report = analyze_skill_confidence(resume_text, detected_skills)
    confidence_by_skill = {
        item["Skill"]: item["Confidence Level"]
        for item in confidence_report
    }
    missing_skills = set(comparison["missing_skills"])

    technical_questions = []
    for skill in required_skills:
        if skill in missing_skills:
            priority = "High"
            evidence_level = "Missing"
            question = (
                f"This role requires {skill}, but your resume does not show it. "
                "How would you answer honestly if the interviewer asks about "
                "your current experience and learning plan?"
            )
            answer_prompt = (
                "Current truth: state your real level; Relevant foundation: "
                "connect only proven skills; Plan: name a concrete next step; "
                "Boundary: do not claim hands-on experience you do not have."
            )
        else:
            evidence_level = confidence_by_skill.get(skill, "Weak Evidence")
            if evidence_level == "Strong Evidence":
                priority = "Practice"
                question = (
                    f"Walk me through a real project or task where you used {skill}. "
                    "What problem did you solve, what did you personally do, and "
                    "what was the result?"
                )
            else:
                priority = "High" if evidence_level == "Weak Evidence" else "Medium"
                question = (
                    f"Your resume mentions {skill} with limited detail. What is "
                    "your strongest real example, and what can you prove about "
                    "your contribution?"
                )
            answer_prompt = (
                "Situation: real context; Task: your responsibility; Action: "
                f"what you personally did with {skill}; Result: truthful outcome; "
                "Proof: artifact, metric, or explanation you can defend."
            )

        technical_questions.append(
            {
                "Priority": priority,
                "Skill": skill,
                "Resume Evidence": evidence_level,
                "Interview Question": question,
                "Answer Structure": answer_prompt,
            }
        )

    priority_order = {"High": 0, "Medium": 1, "Practice": 2}
    technical_questions.sort(key=lambda item: priority_order[item["Priority"]])

    behavioral_questions = [
        {
            "Competency": "Communication",
            "Interview Question": (
                "Tell me about a time you explained a technical finding to a "
                "non-technical stakeholder."
            ),
            "STAR + Proof Prompt": (
                "Situation; Task; Action; Result; name the real presentation, "
                "report, dashboard, feedback, or decision that supports the story."
            ),
        },
        {
            "Competency": "Problem Solving",
            "Interview Question": (
                "Describe a difficult technical problem you diagnosed and solved."
            ),
            "STAR + Proof Prompt": (
                "Situation; Task; diagnostic steps; your specific action; truthful "
                "result; evidence you can explain or show."
            ),
        },
        {
            "Competency": "Learning Agility",
            "Interview Question": (
                "Tell me how you would close a required-skill gap while remaining "
                "honest about your current level."
            ),
            "STAR + Proof Prompt": (
                "Current gap; relevant foundation; learning plan; practice project; "
                "verification milestone; do not claim unearned experience."
            ),
        },
        {
            "Competency": "Ownership",
            "Interview Question": (
                "Tell me about a time you took ownership of a project from unclear "
                "requirements through delivery."
            ),
            "STAR + Proof Prompt": (
                "Situation; Task; decisions you owned; collaboration; delivered "
                "result; real artifact, metric, or stakeholder outcome."
            ),
        },
    ]

    high_priority_count = sum(
        item["Priority"] == "High" for item in technical_questions
    )
    missing_skill_count = len(comparison["missing_skills"])
    status = (
        f"Practice {len(technical_questions)} technical and "
        f"{len(behavioral_questions)} behavioral questions. Start with "
        f"{high_priority_count} high-priority question(s)."
    )

    return {
        "required_skill_count": len(required_skills),
        "technical_question_count": len(technical_questions),
        "behavioral_question_count": len(behavioral_questions),
        "high_priority_question_count": high_priority_count,
        "missing_skill_count": missing_skill_count,
        "status": status,
        "technical_questions": technical_questions,
        "behavioral_questions": behavioral_questions,
        "truthfulness_note": (
            "Never invent interview answers, experience, projects, or measurable "
            "results. Practice only stories you can explain and prove. For missing "
            "skills, state your current level honestly and describe a concrete "
            "learning plan."
        ),
    }
