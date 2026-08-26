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


REQUIREMENT_EVIDENCE_ACTION_WORDS = (
    "built",
    "created",
    "developed",
    "implemented",
    "designed",
    "used",
    "applied",
    "analyzed",
    "analysed",
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
    "documented",
    "tested",
    "validated",
    "reconciled",
    "optimized",
    "improved",
)

REQUIREMENT_EVIDENCE_CONTEXT_WORDS = (
    "experience",
    "worked with",
    "hands on",
    "project",
    "projects",
    "portfolio",
    "support",
    "dashboard",
    "dashboards",
    "report",
    "reports",
    "pipeline",
    "pipelines",
    "model",
    "models",
    "query",
    "queries",
    "analysis",
    "test",
    "testing",
    "application",
    "applications",
    "system",
    "systems",
    "dataset",
    "datasets",
    "data",
    "process",
    "workflow",
    "workflows",
    "validation",
    "reconciliation",
    "stakeholder",
    "client",
    "clients",
    "customer",
    "customers",
    "team",
    "teams",
)

REQUIREMENT_EVIDENCE_OUTCOME_WORDS = (
    "result",
    "resulting",
    "outcome",
    "impact",
    "improved",
    "reduced",
    "increased",
    "saved",
    "accuracy",
    "efficiency",
    "performance",
    "delivered",
    "produced",
)

REQUIREMENT_EVIDENCE_WEIGHTS = {
    "Strong Evidence": 1.0,
    "Moderate Evidence": 0.65,
    "Mention Only": 0.25,
    "Missing": 0.0,
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
        r"\b(?:preferred|nice to have|bonus|desirable|optional|a plus|plus)\b",
        _normalize_skill_text(text),
    ) is not None


REQUIRED_SKILL_MARKERS = re.compile(
    r"\b(?:required|must|required skills?|minimum qualifications?|"
    r"strong(?:ly)?|advanced|proficien(?:t|cy)|hands on|"
    r"experience (?:with|using|in)|responsibilities?)\b"
)


def _job_skill_statements(text):
    """Yield job-posting statements while preserving section intent."""
    section_type = None
    for raw_line in re.split(r"[\r\n]+", str(text or "")):
        line = raw_line.strip(" \t-*•")
        if not line:
            continue

        normalized_line = _normalize_skill_text(line)
        heading_text = normalized_line.rstrip(":")
        heading_word_count = len(heading_text.split())
        is_heading = line.rstrip().endswith(":") and heading_word_count <= 5

        if is_heading and re.search(
            r"\b(?:preferred|nice to have|optional|bonus|desirable)\b",
            heading_text,
        ):
            section_type = "preferred"
            continue
        if is_heading and re.search(
            r"\b(?:requirements?|required skills?|qualifications?|"
            r"minimum qualifications?|responsibilities?)\b",
            heading_text,
        ):
            section_type = "required"
            continue

        statements = re.split(r"(?<=[.!?;])\s+|\s*;\s*", line)
        for statement in statements:
            statement = statement.strip(" \t-*•")
            if statement:
                yield statement, section_type


def classify_job_skills(job_description_text):
    """Separate required skills from optional or preferred job skills.

    Explicit preference language wins for its statement. Skills mentioned in
    requirements/responsibilities sections or with mandatory language are
    required. Unmarked skills remain required to preserve useful behavior for
    short, informal job descriptions. If a skill appears in both groups,
    required wins.
    """
    all_skills = detect_skills(job_description_text)
    required_candidates = []
    preferred_candidates = []
    unmarked_candidates = []
    explicit_preference_found = False

    for statement, section_type in _job_skill_statements(job_description_text):
        statement_skills = detect_skills(statement)
        if not statement_skills:
            continue

        normalized_statement = _normalize_skill_text(statement)
        if _is_optional_requirement(statement) or section_type == "preferred":
            explicit_preference_found = True
            preferred_candidates.extend(statement_skills)
        elif REQUIRED_SKILL_MARKERS.search(normalized_statement) or section_type == "required":
            required_candidates.extend(statement_skills)
        else:
            unmarked_candidates.extend(statement_skills)

    # A practical mention without preference language is treated as required.
    # This also keeps older, comma-separated sample descriptions meaningful.
    required_set = set(required_candidates) | set(unmarked_candidates)
    preferred_set = set(preferred_candidates) - required_set
    required_skills = [skill for skill in all_skills if skill in required_set]
    preferred_skills = [skill for skill in all_skills if skill in preferred_set]

    # Defensive fallback for text that the statement parser could not segment.
    classified = set(required_skills) | set(preferred_skills)
    required_skills.extend(
        skill for skill in all_skills if skill not in classified
    )

    return {
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "all_skills": all_skills,
        "classification_method": (
            "explicit_preference_markers"
            if explicit_preference_found
            else "unmarked_skills_treated_as_required"
        ),
        "disclaimer": (
            "Preferred skills are shown separately and do not lower the "
            "required-skill match. Verify ambiguous wording against the "
            "original posting."
        ),
    }


def analyze_job_description(job_description_text):
    return classify_job_skills(job_description_text)["required_skills"]


def _source_evidence_statements(text):
    """Split source text into readable excerpts while preserving its wording."""
    statements = []
    for raw_line in re.split(r"[\r\n]+", str(text or "")):
        line = raw_line.strip(" \t-*•")
        if not line:
            continue
        for match in re.finditer(r"[^.!?;]+(?:[.!?;]+|$)", line):
            statement = match.group(0).strip(" \t-*•")
            if statement:
                statements.append(statement)
    return statements


def _evidence_excerpt(statement, maximum_length=320):
    statement = re.sub(r"\s+", " ", str(statement or "")).strip()
    if len(statement) <= maximum_length:
        return statement
    return statement[: maximum_length - 1].rstrip() + "…"


def _resume_skill_evidence(resume_text, skill):
    action_words = (
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
        "documented",
        "tested",
        "validated",
    )
    experience_words = (
        "experience",
        "worked with",
        "hands on",
        "project",
        "portfolio",
        "support",
    )

    candidates = []
    for index, statement in enumerate(_source_evidence_statements(resume_text)):
        if skill not in detect_skills(statement):
            continue
        normalized_statement = _normalize_skill_text(statement)
        evidence_strength = 0
        if any(
            _contains_skill_keyword(normalized_statement, word)
            for word in action_words
        ):
            evidence_strength = 2
        elif any(word in normalized_statement for word in experience_words):
            evidence_strength = 1
        candidates.append(
            (evidence_strength, len(statement), -index, statement)
        )

    if not candidates:
        return None
    strongest_statement = max(candidates)[-1]
    return _evidence_excerpt(strongest_statement)


def _job_skill_evidence(job_description_text, skill, requirement_type):
    candidates = []
    for index, (statement, section_type) in enumerate(
        _job_skill_statements(job_description_text)
    ):
        if skill not in detect_skills(statement):
            continue

        normalized_statement = _normalize_skill_text(statement)
        is_preferred = (
            _is_optional_requirement(statement)
            or section_type == "preferred"
        )
        is_explicitly_required = (
            section_type == "required"
            or REQUIRED_SKILL_MARKERS.search(normalized_statement) is not None
        )
        if requirement_type == "Preferred":
            classification_strength = 2 if is_preferred else 0
        elif is_preferred:
            classification_strength = 0
        elif is_explicitly_required:
            classification_strength = 2
        else:
            classification_strength = 1

        candidates.append(
            (classification_strength, len(statement), -index, statement)
        )

    if not candidates:
        return None
    strongest_statement = max(candidates)[-1]
    return _evidence_excerpt(strongest_statement)


def generate_evidence_traceability(
    resume_text,
    job_description_text,
    job_skill_requirements=None,
):
    """Trace every detected job skill to exact résumé and posting excerpts."""
    job_skill_requirements = job_skill_requirements or classify_job_skills(
        job_description_text
    )
    rows = []

    for requirement_type, skills in (
        ("Required", job_skill_requirements.get("required_skills", [])),
        ("Preferred", job_skill_requirements.get("preferred_skills", [])),
    ):
        for skill in skills:
            resume_evidence = _resume_skill_evidence(resume_text, skill)
            job_evidence = _job_skill_evidence(
                job_description_text,
                skill,
                requirement_type,
            )
            rows.append(
                {
                    "Requirement": skill,
                    "Type": requirement_type,
                    "Status": (
                        "Matched"
                        if resume_evidence and requirement_type == "Required"
                        else "Present"
                        if resume_evidence
                        else "Missing"
                        if requirement_type == "Required"
                        else "Opportunity"
                    ),
                    "Résumé Evidence": (
                        resume_evidence
                        or "No supporting résumé excerpt detected."
                    ),
                    "Job Evidence": (
                        job_evidence
                        or "No isolated job-posting excerpt was found."
                    ),
                }
            )

    required_rows = [row for row in rows if row["Type"] == "Required"]
    preferred_rows = [row for row in rows if row["Type"] == "Preferred"]
    matched_count = sum(
        row["Status"] in {"Matched", "Present"} for row in rows
    )

    return {
        "rows": rows,
        "required_rows": required_rows,
        "preferred_rows": preferred_rows,
        "matched_count": matched_count,
        "missing_count": len(rows) - matched_count,
        "disclaimer": (
            "Excerpts are copied from the pasted résumé and job posting. A "
            "keyword excerpt shows textual support, not verified proficiency, "
            "experience duration, or employer endorsement."
        ),
    }


def _looks_like_bare_skill_list(resume_evidence):
    """Return True when an excerpt names skills without résumé evidence."""
    normalized_evidence = _normalize_skill_text(resume_evidence)
    detected_skills = detect_skills(resume_evidence)
    has_action = any(
        _contains_skill_keyword(normalized_evidence, word)
        for word in REQUIREMENT_EVIDENCE_ACTION_WORDS
    )
    has_outcome = any(
        _contains_skill_keyword(normalized_evidence, word)
        for word in REQUIREMENT_EVIDENCE_OUTCOME_WORDS
    ) or re.search(r"\b\d+(?:[.,]\d+)?%?\b", normalized_evidence) is not None
    has_explicit_context = re.search(
        r"\b(?:experience|worked with|hands on|project|projects|portfolio|"
        r"responsible for|supported)\b",
        normalized_evidence,
    ) is not None

    if has_action or has_outcome or has_explicit_context:
        return False

    has_skill_heading = re.match(
        r"^(?:technical |core )?(?:skills?|technologies|tools|competencies)\b",
        normalized_evidence,
    ) is not None
    has_comma_separated_skills = (
        len(detected_skills) >= 3 and str(resume_evidence).count(",") >= 2
    )
    return has_skill_heading or has_comma_separated_skills


def _requirement_evidence_level(resume_evidence):
    """Classify one exact résumé excerpt without inferring missing facts."""
    if not resume_evidence:
        return (
            "Missing",
            "No supporting résumé excerpt was detected for this requirement.",
        )

    if _looks_like_bare_skill_list(resume_evidence):
        return (
            "Mention Only",
            "The skill is listed or named without an action, project, experience "
            "example, or outcome.",
        )

    normalized_evidence = _normalize_skill_text(resume_evidence)
    has_action = any(
        _contains_skill_keyword(normalized_evidence, word)
        for word in REQUIREMENT_EVIDENCE_ACTION_WORDS
    )
    has_context = any(
        _contains_skill_keyword(normalized_evidence, word)
        for word in REQUIREMENT_EVIDENCE_CONTEXT_WORDS
    )
    has_outcome = any(
        _contains_skill_keyword(normalized_evidence, word)
        for word in REQUIREMENT_EVIDENCE_OUTCOME_WORDS
    ) or re.search(r"\b\d+(?:[.,]\d+)?%?\b", normalized_evidence) is not None

    if has_action and (has_context or has_outcome):
        return (
            "Strong Evidence",
            "The excerpt shows practical use through an action and a concrete "
            "task, deliverable, context, or outcome.",
        )
    if has_action or has_context:
        return (
            "Moderate Evidence",
            "The excerpt adds action or experience context, but practical "
            "scope and results remain limited.",
        )
    return (
        "Mention Only",
        "The skill is listed or named without an action, project, experience "
        "example, or outcome.",
    )


def analyze_requirement_evidence_strength(
    resume_text,
    job_description_text,
    job_skill_requirements=None,
):
    """Evaluate evidence quality for required skills without changing scores."""
    job_skill_requirements = job_skill_requirements or classify_job_skills(
        job_description_text
    )
    rows = []

    for skill in job_skill_requirements.get("required_skills", []):
        resume_evidence = _resume_skill_evidence(resume_text, skill)
        strength, reason = _requirement_evidence_level(resume_evidence)
        rows.append(
            {
                "Requirement": skill,
                "Evidence Strength": strength,
                "Résumé Evidence": (
                    resume_evidence
                    or "No supporting résumé excerpt detected."
                ),
                "Why": reason,
            }
        )

    counts = {
        level: sum(row["Evidence Strength"] == level for row in rows)
        for level in (
            "Strong Evidence",
            "Moderate Evidence",
            "Mention Only",
            "Missing",
        )
    }

    if counts["Missing"]:
        next_step = (
            "Address missing requirements first. Add them to the résumé only "
            "after you have truthful evidence you can explain and prove."
        )
    elif counts["Mention Only"]:
        next_step = (
            "Replace skill-list-only mentions with truthful examples of how "
            "you used each skill."
        )
    elif counts["Moderate Evidence"]:
        next_step = (
            "Strengthen moderate evidence with truthful scope, ownership, "
            "deliverables, or measurable outcomes."
        )
    elif rows:
        next_step = (
            "Preserve the action-based evidence and prepare to explain each "
            "example in an interview."
        )
    else:
        next_step = (
            "Paste a complete job description so required skills can be "
            "evaluated."
        )

    return {
        "rows": rows,
        "strong_count": counts["Strong Evidence"],
        "moderate_count": counts["Moderate Evidence"],
        "mention_only_count": counts["Mention Only"],
        "missing_count": counts["Missing"],
        "next_step": next_step,
        "disclaimer": (
            "Evidence strength evaluates résumé wording only; it does not "
            "verify proficiency, experience duration, or employer endorsement. "
            "It does not change the three existing match scores."
        ),
    }


def calculate_evidence_adjusted_requirement_score(evidence_strength):
    """Score required skills by evidence quality, not keyword presence alone."""
    rows = list(evidence_strength.get("rows", []))
    total_requirements = len(rows)
    level_counts = {
        level: sum(row.get("Evidence Strength") == level for row in rows)
        for level in REQUIREMENT_EVIDENCE_WEIGHTS
    }
    earned_points = sum(
        REQUIREMENT_EVIDENCE_WEIGHTS.get(
            row.get("Evidence Strength"),
            0.0,
        )
        for row in rows
    )
    score = (
        round((earned_points / total_requirements) * 100, 2)
        if total_requirements
        else 0.0
    )

    if not total_requirements:
        status = "Not Enough Requirements"
        next_step = (
            "Paste a complete job description so required-skill evidence can "
            "be scored."
        )
    elif score >= 85:
        status = "Strong Evidence Coverage"
        next_step = (
            "Preserve the strongest evidence and prepare to explain each "
            "example with truthful scope and outcomes."
        )
    elif score >= 65:
        status = "Competitive Evidence Coverage"
        next_step = (
            "Address missing requirements, then strengthen mention-only and "
            "moderate evidence with truthful examples."
        )
    elif score >= 40:
        status = "Developing Evidence Coverage"
        next_step = (
            "Prioritize missing requirements and replace skill-list mentions "
            "with truthful project or work evidence."
        )
    else:
        status = "Limited Evidence Coverage"
        next_step = (
            "Build and document truthful evidence for the highest-priority "
            "requirements before presenting the résumé as a strong match."
        )

    breakdown = []
    for level, weight in REQUIREMENT_EVIDENCE_WEIGHTS.items():
        count = level_counts[level]
        breakdown.append(
            {
                "Evidence Level": level,
                "Weight": f"{weight * 100:.0f}%",
                "Requirements": count,
                "Earned Points": round(count * weight, 2),
            }
        )

    return {
        "score": score,
        "status": status,
        "total_requirements": total_requirements,
        "earned_points": round(earned_points, 2),
        "breakdown": breakdown,
        "next_step": next_step,
        "methodology": (
            "Strong Evidence = 100%, Moderate Evidence = 65%, Mention Only = "
            "25%, and Missing = 0%. The score is the average weight across "
            "required skills only."
        ),
        "disclaimer": (
            "This separate evidence-quality score does not change Job "
            "Description Match, Semantic Match, or Target Career Match. It "
            "evaluates résumé wording, not verified proficiency or an employer "
            "decision."
        ),
    }


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


def calculate_analysis_confidence(
    input_quality,
    job_comparison,
    critical_requirements,
):
    """Estimate how much evidence supports the reliability of an analysis.

    Confidence is deliberately separate from candidate fit. A clearly missing
    skill can be a high-confidence finding, while a perfect match produced from
    very short inputs can still have low confidence.
    """
    input_quality = input_quality or {}
    job_comparison = job_comparison or {}
    critical_requirements = critical_requirements or {}

    resume_word_count = int(input_quality.get("resume_word_count", 0) or 0)
    job_word_count = int(input_quality.get("job_word_count", 0) or 0)
    resume_skill_count = int(input_quality.get("resume_skill_count", 0) or 0)
    required_skill_count = len(job_comparison.get("matched_skills", [])) + len(
        job_comparison.get("missing_skills", [])
    )

    met_count = int(critical_requirements.get("met_count", 0) or 0)
    unclear_count = int(critical_requirements.get("unclear_count", 0) or 0)
    missing_count = int(critical_requirements.get("missing_count", 0) or 0)
    critical_count = met_count + unclear_count + missing_count

    resume_detail_points = min(25.0, (resume_word_count / 120) * 25)
    job_detail_points = min(25.0, (job_word_count / 100) * 25)
    requirement_points = min(15.0, (required_skill_count / 8) * 15)
    resume_skill_points = min(10.0, (resume_skill_count / 8) * 10)

    if critical_count:
        resolved_critical_count = met_count + missing_count
        critical_certainty_points = (
            resolved_critical_count / critical_count
        ) * 25
        critical_evidence = (
            f"{resolved_critical_count} of {critical_count} critical "
            "requirements have a resolved Met or Missing status."
        )
    else:
        critical_certainty_points = 25.0
        critical_evidence = (
            "No explicit critical requirements need an Unclear status."
        )

    confidence_score = round(
        resume_detail_points
        + job_detail_points
        + requirement_points
        + resume_skill_points
        + critical_certainty_points,
        2,
    )

    if confidence_score >= 80:
        confidence_level = "High"
        message_type = "success"
        headline = (
            "High confidence: the inputs provide substantial evidence for the "
            "current analysis."
        )
        next_step = (
            "Verify the extracted evidence, then use the scores as guidance for "
            "truthful résumé tailoring and interview preparation."
        )
    elif confidence_score >= 60:
        confidence_level = "Moderate"
        message_type = "info"
        headline = (
            "Moderate confidence: the analysis is useful, but some evidence "
            "limitations should be reviewed."
        )
        next_step = (
            "Review the listed limitations and resolve unclear evidence before "
            "making an application decision."
        )
    else:
        confidence_level = "Low"
        message_type = "warning"
        headline = (
            "Low confidence: treat the match scores as preliminary rather than "
            "a complete evaluation."
        )
        next_step = (
            "Paste the complete résumé and job posting, then rerun the analysis."
        )

    limitations = []
    if resume_word_count < 120:
        limitations.append(
            f"Résumé detail is limited ({resume_word_count} words; 120+ gives "
            "the analyzer stronger evidence)."
        )
    if job_word_count < 100:
        limitations.append(
            f"Job-posting detail is limited ({job_word_count} words; 100+ gives "
            "the analyzer stronger evidence)."
        )
    if required_skill_count < 5:
        limitations.append(
            f"Only {required_skill_count} required skill(s) were detected, so "
            "the skill-match sample is small."
        )
    if resume_skill_count < 5:
        limitations.append(
            f"Only {resume_skill_count} résumé skill(s) were detected."
        )
    if unclear_count:
        limitations.append(
            f"{unclear_count} critical requirement(s) remain Unclear and need "
            "human verification."
        )

    factors = [
        {
            "Confidence Factor": "Résumé detail",
            "Evidence": f"{resume_word_count} words",
            "Contribution": f"{resume_detail_points:.2f} / 25",
        },
        {
            "Confidence Factor": "Job-posting detail",
            "Evidence": f"{job_word_count} words",
            "Contribution": f"{job_detail_points:.2f} / 25",
        },
        {
            "Confidence Factor": "Required-skill sample",
            "Evidence": f"{required_skill_count} detected",
            "Contribution": f"{requirement_points:.2f} / 15",
        },
        {
            "Confidence Factor": "Résumé skill evidence",
            "Evidence": f"{resume_skill_count} detected",
            "Contribution": f"{resume_skill_points:.2f} / 10",
        },
        {
            "Confidence Factor": "Critical-evidence certainty",
            "Evidence": critical_evidence,
            "Contribution": f"{critical_certainty_points:.2f} / 25",
        },
    ]

    return {
        "confidence_level": confidence_level,
        "confidence_score": confidence_score,
        "message_type": message_type,
        "headline": headline,
        "factors": factors,
        "limitations": limitations,
        "next_step": next_step,
        "disclaimer": (
            "Analysis Confidence measures evidence completeness and certainty. "
            "It does not measure candidate quality or guarantee an employer "
            "decision."
        ),
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
    evidence_adjusted_score=None,
    analysis_confidence=None,
):
    """Create a cautious application recommendation from existing evidence.

    The three match scores remain independent inputs. Optional evidence-quality
    and analysis-confidence results can only make the recommendation more
    cautious; they can never upgrade it.
    """
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

    original_decision = decision
    guardrail_reasons = []
    maximum_decision = None
    decision_rank = {
        "Improve Before Applying": 0,
        "Consider Applying": 1,
        "Strong Match": 2,
    }

    evidence_adjusted_score = evidence_adjusted_score or {}
    evidence_requirement_count = int(
        evidence_adjusted_score.get("total_requirements", 0) or 0
    )
    if evidence_requirement_count:
        evidence_score_value = float(
            evidence_adjusted_score.get("score", 0) or 0
        )
        evidence_status = evidence_adjusted_score.get(
            "status",
            "Evidence Coverage",
        )
        reasons.append(
            "Evidence quality: the evidence-adjusted required-skill score is "
            f"{round(evidence_score_value, 2)}% ({evidence_status})."
        )
        if evidence_score_value < 40:
            maximum_decision = "Improve Before Applying"
            guardrail_reasons.append(
                "Required-skill evidence coverage is below 40%, so the "
                "recommendation cannot exceed Improve Before Applying."
            )
        elif evidence_score_value < 65:
            maximum_decision = "Consider Applying"
            guardrail_reasons.append(
                "Required-skill evidence coverage is below 65%, so the "
                "recommendation cannot be Strong Match."
            )

    analysis_confidence = analysis_confidence or {}
    confidence_level = analysis_confidence.get("confidence_level")
    confidence_score = analysis_confidence.get("confidence_score")
    if confidence_level:
        confidence_text = f"Analysis reliability: confidence is {confidence_level}"
        if confidence_score is not None:
            confidence_text += f" ({round(float(confidence_score), 2)}%)"
        reasons.append(confidence_text + ".")
    if confidence_level == "Low":
        low_confidence_cap = "Consider Applying"
        if (
            maximum_decision is None
            or decision_rank[low_confidence_cap]
            < decision_rank[maximum_decision]
        ):
            maximum_decision = low_confidence_cap
        guardrail_reasons.append(
            "Analysis Confidence is Low, so the available inputs do not "
            "support a Strong Match recommendation."
        )

    guardrail_applied = False
    if (
        maximum_decision is not None
        and decision in decision_rank
        and decision_rank[decision] > decision_rank[maximum_decision]
    ):
        decision = maximum_decision
        guardrail_applied = True
        if decision == "Improve Before Applying":
            message_type = "warning"
            headline = (
                "The detected skills need stronger truthful résumé evidence "
                "before this should be treated as an application-ready match."
            )
            next_action = (
                "Build or document truthful evidence for the missing and "
                "weakly supported required skills, then rerun the analysis."
            )
        else:
            message_type = "info"
            headline = (
                "The skill alignment is promising, but the available evidence "
                "does not support a Strong Match recommendation yet."
            )
            next_action = (
                "Review the evidence limitations and strengthen required-skill "
                "examples truthfully before relying on a stronger recommendation."
            )

    if guardrail_applied:
        guardrail_status = "Recommendation Adjusted"
        guardrail_summary = (
            f"The evidence-aware guardrail changed {original_decision} to "
            f"{decision}."
        )
    elif guardrail_reasons:
        guardrail_status = "Caution Confirmed"
        guardrail_summary = (
            "The evidence-aware guardrail supports the current cautious "
            "recommendation."
        )
    else:
        guardrail_status = "No Adjustment Needed"
        guardrail_summary = (
            "No evidence-quality or confidence condition required a more "
            "cautious recommendation."
        )

    return {
        "decision": decision,
        "original_decision": original_decision,
        "message_type": message_type,
        "headline": headline,
        "reasons": reasons,
        "next_action": next_action,
        "critical_support_score": critical_support_score,
        "blocking_requirements": blocking_requirements,
        "guardrail_applied": guardrail_applied,
        "guardrail_status": guardrail_status,
        "guardrail_summary": guardrail_summary,
        "guardrail_reasons": guardrail_reasons,
        "maximum_recommendation": maximum_decision,
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
    job_skill_requirements = classify_job_skills(job_description_text)
    job_required_skills = job_skill_requirements["required_skills"]
    job_preferred_skills = job_skill_requirements["preferred_skills"]
    matched_required_skills = [
        skill for skill in job_required_skills if skill in resume_skills
    ]
    matched_preferred_skills = [
        skill for skill in job_preferred_skills if skill in resume_skills
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
        "matched_preferred_skills": matched_preferred_skills,
        "matched_preferred_skill_count": len(matched_preferred_skills),
        "preferred_skill_count": len(job_preferred_skills),
        "scoring_method": scoring_method,
    }


def calculate_semantic_match_score(resume_text, job_description_text):
    return calculate_semantic_match_details(
        resume_text,
        job_description_text,
    )["semantic_score"]


SAVED_ANALYSIS_EVIDENCE_RANKS = {
    "Missing": 0,
    "Mention Only": 1,
    "Moderate Evidence": 2,
    "Strong Evidence": 3,
}

SAVED_ANALYSIS_PROGRESS_METRICS = (
    ("Job Description Match", "job_description_match"),
    ("Semantic Match", "semantic_match"),
    ("Target Career Match", "target_career_match"),
    ("Evidence-Adjusted Score", "evidence_adjusted_score"),
)


def _saved_analysis_snapshot(record):
    """Normalize one saved analysis using the current TalentBridge rules."""
    result_data = record.get("result_data") or {}
    resume_text = result_data.get("resume_text", "")
    job_description_text = result_data.get("job_description_text", "")
    target_career = (
        result_data.get("target_career")
        or record.get("target_career")
        or ""
    )

    resume_skills = (
        analyze_resume_text(resume_text)
        if resume_text.strip()
        else list(result_data.get("resume_skills", []))
    )
    if job_description_text.strip():
        job_skill_requirements = classify_job_skills(job_description_text)
    else:
        job_skill_requirements = result_data.get(
            "job_skill_requirements",
            {
                "required_skills": result_data.get("job_required_skills", []),
                "preferred_skills": result_data.get("job_preferred_skills", []),
            },
        )

    required_skills = job_skill_requirements.get("required_skills", [])
    if required_skills or job_description_text.strip():
        job_comparison = compare_resume_to_job(resume_skills, required_skills)
    else:
        job_comparison = result_data.get(
            "job_comparison",
            {"matched_skills": [], "missing_skills": [], "match_score": 0},
        )

    if resume_text.strip() and job_description_text.strip():
        semantic_score = calculate_semantic_match_details(
            resume_text,
            job_description_text,
        )["semantic_score"]
        evidence_strength = analyze_requirement_evidence_strength(
            resume_text,
            job_description_text,
            job_skill_requirements,
        )
    else:
        semantic_score = float(result_data.get("semantic_match_score", 0) or 0)
        evidence_strength = result_data.get(
            "requirement_evidence_strength",
            {"rows": []},
        )

    evidence_score = calculate_evidence_adjusted_requirement_score(
        evidence_strength
    )["score"]
    try:
        target_career_score = calculate_target_career_match(
            resume_skills,
            target_career,
        )["match_score"]
    except ValueError:
        target_career_score = float(
            result_data.get("target_career_match_score", 0) or 0
        )

    evidence_levels = {
        row.get("Requirement", ""): row.get("Evidence Strength", "Missing")
        for row in evidence_strength.get("rows", [])
        if row.get("Requirement")
    }
    return {
        "id": str(record.get("id", "")),
        "created_at": str(record.get("created_at", "")),
        "target_career": target_career,
        "job_title": result_data.get("job_title", "") or "Saved Job",
        "job_description_text": job_description_text,
        "job_description_match": float(job_comparison.get("match_score", 0) or 0),
        "semantic_match": float(semantic_score or 0),
        "target_career_match": float(target_career_score or 0),
        "evidence_adjusted_score": float(evidence_score or 0),
        "matched_skills": list(job_comparison.get("matched_skills", [])),
        "missing_skills": list(job_comparison.get("missing_skills", [])),
        "evidence_levels": evidence_levels,
    }


def compare_saved_analyses(before_record, after_record):
    """Compare two private saved analyses without changing either record."""
    before = _saved_analysis_snapshot(before_record)
    after = _saved_analysis_snapshot(after_record)
    metrics = (
        ("Job Description Match", "job_description_match"),
        ("Semantic Match", "semantic_match"),
        ("Target Career Match", "target_career_match"),
        ("Evidence-Adjusted Score", "evidence_adjusted_score"),
    )
    score_rows = []
    score_deltas = {}
    for label, key in metrics:
        delta = round(after[key] - before[key], 2)
        score_deltas[key] = delta
        score_rows.append(
            {
                "Metric": label,
                "Before": f"{before[key]:.2f}%",
                "After": f"{after[key]:.2f}%",
                "Change": f"{delta:+.2f} points",
            }
        )

    before_matched = set(before["matched_skills"])
    after_matched = set(after["matched_skills"])
    newly_matched = sorted(after_matched - before_matched)
    no_longer_matched = sorted(before_matched - after_matched)

    evidence_improved = []
    evidence_weakened = []
    shared_requirements = set(before["evidence_levels"]) & set(
        after["evidence_levels"]
    )
    for skill in sorted(shared_requirements):
        before_level = before["evidence_levels"][skill]
        after_level = after["evidence_levels"][skill]
        before_rank = SAVED_ANALYSIS_EVIDENCE_RANKS.get(before_level, 0)
        after_rank = SAVED_ANALYSIS_EVIDENCE_RANKS.get(after_level, 0)
        change = f"{skill}: {before_level} → {after_level}"
        if after_rank > before_rank:
            evidence_improved.append(change)
        elif after_rank < before_rank:
            evidence_weakened.append(change)

    job_delta = score_deltas["job_description_match"]
    if job_delta > 0:
        summary = (
            f"Required-skill match improved by {job_delta:.2f} points."
        )
    elif job_delta < 0:
        summary = (
            f"Required-skill match decreased by {abs(job_delta):.2f} points."
        )
    else:
        summary = "Required-skill match did not change."
    if newly_matched:
        summary += f" Newly matched: {', '.join(newly_matched)}."
    if after["missing_skills"]:
        summary += (
            " Remaining gaps: " + ", ".join(after["missing_skills"]) + "."
        )
    else:
        summary += " No required-skill gaps remain in the after analysis."

    return {
        "before": before,
        "after": after,
        "score_rows": score_rows,
        "score_deltas": score_deltas,
        "newly_matched_skills": newly_matched,
        "no_longer_matched_skills": no_longer_matched,
        "remaining_gaps": after["missing_skills"],
        "evidence_improved": evidence_improved,
        "evidence_weakened": evidence_weakened,
        "same_target_career": (
            before["target_career"] == after["target_career"]
        ),
        "same_job_description": (
            _normalize_skill_text(before["job_description_text"])
            == _normalize_skill_text(after["job_description_text"])
        ),
        "summary": summary,
        "disclaimer": (
            "This comparison uses the current TalentBridge rules on saved "
            "inputs. It measures résumé evidence changes, not verified skill "
            "growth or an employer decision."
        ),
    }


def build_saved_analysis_progress_dashboard(records, target_career=None):
    """Build chronological progress groups from private saved analyses.

    Analyses are comparable only when they use the same target career and the
    same normalized job description. Mixed postings are deliberately kept in
    separate groups so a score change is not mistaken for resume progress.
    """
    snapshots = [_saved_analysis_snapshot(record) for record in records]
    if target_career:
        snapshots = [
            snapshot
            for snapshot in snapshots
            if snapshot["target_career"] == target_career
        ]
    snapshots.sort(key=lambda item: (item["created_at"], item["id"]))

    grouped_snapshots = {}
    records_without_job_text = 0
    for snapshot in snapshots:
        job_key = _normalize_skill_text(snapshot["job_description_text"])
        if not job_key:
            records_without_job_text += 1
            continue
        grouped_snapshots.setdefault(job_key, []).append(snapshot)

    comparable_groups = []
    singleton_count = 0
    for job_snapshots in grouped_snapshots.values():
        if len(job_snapshots) < 2:
            singleton_count += len(job_snapshots)
            continue

        earliest = job_snapshots[0]
        latest = job_snapshots[-1]
        metric_rows = []
        for label, key in SAVED_ANALYSIS_PROGRESS_METRICS:
            delta = round(latest[key] - earliest[key], 2)
            metric_rows.append(
                {
                    "Metric": label,
                    "Earliest": f"{earliest[key]:.2f}%",
                    "Latest": f"{latest[key]:.2f}%",
                    "Change": f"{delta:+.2f} points",
                    "latest_value": latest[key],
                    "delta_value": delta,
                }
            )

        trend_rows = []
        for index, snapshot in enumerate(job_snapshots, start=1):
            saved_at = snapshot["created_at"][:16].replace("T", " ")
            trend_rows.append(
                {
                    "Saved At": saved_at or f"Analysis {index}",
                    **{
                        label: snapshot[key]
                        for label, key in SAVED_ANALYSIS_PROGRESS_METRICS
                    },
                }
            )

        earliest_matched = set(earliest["matched_skills"])
        latest_matched = set(latest["matched_skills"])
        job_title = latest["job_title"] or earliest["job_title"]
        date_start = earliest["created_at"][:10] or "unknown date"
        date_end = latest["created_at"][:10] or "unknown date"
        comparable_groups.append(
            {
                "job_title": job_title,
                "label": (
                    f"{job_title} — {len(job_snapshots)} analyses — "
                    f"{date_start} to {date_end}"
                ),
                "analysis_count": len(job_snapshots),
                "analyses": job_snapshots,
                "earliest": earliest,
                "latest": latest,
                "metric_rows": metric_rows,
                "trend_rows": trend_rows,
                "skills_gained": sorted(latest_matched - earliest_matched),
                "skills_no_longer_matched": sorted(
                    earliest_matched - latest_matched
                ),
                "remaining_gaps": sorted(latest["missing_skills"]),
            }
        )

    for index, group in enumerate(comparable_groups, start=1):
        group["key"] = f"job-history-{index}"

    excluded_count = singleton_count + records_without_job_text
    warnings = []
    if len(grouped_snapshots) > 1:
        warnings.append(
            f"Saved analyses contain {len(grouped_snapshots)} different job "
            "descriptions. Their histories are shown separately."
        )
    if excluded_count:
        warnings.append(
            f"{excluded_count} saved analysis record(s) are not yet comparable "
            "because the same job description has not been analyzed twice."
        )
    if snapshots and not comparable_groups:
        warnings.append(
            "No comparable history is available yet. Analyze the same job "
            "description at least twice to create a progress trend."
        )

    return {
        "target_career": target_career or "",
        "record_count": len(snapshots),
        "distinct_job_count": len(grouped_snapshots),
        "comparable_record_count": sum(
            group["analysis_count"] for group in comparable_groups
        ),
        "excluded_record_count": excluded_count,
        "groups": comparable_groups,
        "warnings": warnings,
        "disclaimer": (
            "This dashboard re-evaluates private saved inputs with the current "
            "TalentBridge rules. Trends measure resume evidence changes for the "
            "same posting; they do not verify skill growth or predict an employer "
            "decision."
        ),
    }


def select_best_saved_resume_version(progress_group):
    """Select the strongest saved résumé evidence for one comparable job.

    Evidence quality is the primary criterion. Remaining match scores, gap
    count, and recency provide deterministic tie breakers without turning the
    result into an employer or eligibility decision.
    """
    if progress_group is None:
        raise ValueError("Choose a comparable saved-analysis history first.")

    candidates = list(progress_group.get("analyses", []))
    if not candidates:
        for key in ("earliest", "latest"):
            candidate = progress_group.get(key)
            if candidate and candidate not in candidates:
                candidates.append(candidate)
    if not candidates:
        raise ValueError("No saved résumé versions are available to rank.")

    def numeric_value(candidate, key):
        try:
            return float(candidate.get(key, 0) or 0)
        except (TypeError, ValueError):
            return 0.0

    def strong_evidence_count(candidate):
        return sum(
            1
            for level in candidate.get("evidence_levels", {}).values()
            if level == "Strong Evidence"
        )

    def ranking_key(candidate):
        return (
            numeric_value(candidate, "evidence_adjusted_score"),
            strong_evidence_count(candidate),
            numeric_value(candidate, "job_description_match"),
            numeric_value(candidate, "semantic_match"),
            numeric_value(candidate, "target_career_match"),
            -len(candidate.get("missing_skills", [])),
            str(candidate.get("created_at", "")),
            str(candidate.get("id", "")),
        )

    best = max(candidates, key=ranking_key)
    latest = progress_group.get("latest", {})
    evidence_levels = best.get("evidence_levels", {})
    strong_skills = sorted(
        skill
        for skill, level in evidence_levels.items()
        if level == "Strong Evidence"
    )
    if not strong_skills:
        strong_skills = sorted(best.get("matched_skills", []))
    remaining_gaps = sorted(best.get("missing_skills", []))
    evidence_score = numeric_value(best, "evidence_adjusted_score")
    analysis_count = len(candidates)
    saved_at = str(best.get("created_at", ""))
    saved_date = saved_at[:10] or "Unknown date"
    is_latest = bool(
        latest
        and str(best.get("id", "")) == str(latest.get("id", ""))
    )

    reason = (
        f"This version ranks highest among {analysis_count} comparable saved "
        f"versions because the ranking prioritizes its {evidence_score:.2f}% "
        "Evidence-Adjusted Score, then strong evidence, required-skill match, "
        "semantic alignment, career match, fewer gaps, and recency."
    )
    if remaining_gaps:
        priority_gaps = remaining_gaps[:3]
        recommendation = (
            "Use this saved version as the starting point, then strengthen "
            "truthful résumé evidence for "
            f"{', '.join(priority_gaps)}."
        )
    else:
        recommendation = (
            "Use this saved version as the starting point and preserve its "
            "truthful evidence when tailoring the résumé."
        )

    return {
        "analysis_id": str(best.get("id", "")),
        "saved_at": saved_at,
        "saved_date": saved_date,
        "is_latest": is_latest,
        "analysis_count": analysis_count,
        "job_description_match": numeric_value(
            best,
            "job_description_match",
        ),
        "semantic_match": numeric_value(best, "semantic_match"),
        "target_career_match": numeric_value(best, "target_career_match"),
        "evidence_adjusted_score": evidence_score,
        "strong_skills": strong_skills,
        "matched_skills": sorted(best.get("matched_skills", [])),
        "remaining_gaps": remaining_gaps,
        "reason": reason,
        "recommendation": recommendation,
        "disclaimer": (
            "This selection ranks comparable saved résumé evidence under the "
            "current TalentBridge rules. It does not verify proficiency, "
            "predict an employer decision, or guarantee an interview."
        ),
    }


def generate_best_version_application_plan(progress_group, target_career):
    """Create a truthful application plan for the strongest saved version.

    The plan intentionally exports only the derived evidence summary. Private
    résumé text and the full job posting remain in the signed-in user's saved
    records.
    """
    if not progress_group:
        raise ValueError("Choose a comparable saved-analysis history first.")

    best = select_best_saved_resume_version(progress_group)
    career = str(target_career or "Not specified")
    job_title = str(progress_group.get("job_title", "") or "Saved Job")
    strong_skills = list(best.get("strong_skills", []))
    matched_skills = list(best.get("matched_skills", []))
    remaining_gaps = list(best.get("remaining_gaps", []))

    lines = [
        "TalentBridge AI - Best-Version Application Plan",
        "================================================",
        "",
        f"Target Career: {career}",
        f"Job: {job_title}",
        f"Selected Saved Version: {best['saved_date']}",
        f"Comparable Versions Reviewed: {best['analysis_count']}",
        "",
        "Readiness Snapshot",
        "------------------",
        (
            "- Evidence-Adjusted Requirement Score: "
            f"{best['evidence_adjusted_score']:.2f}%"
        ),
        f"- Job Description Match: {best['job_description_match']:.2f}%",
        f"- Semantic Match: {best['semantic_match']:.2f}%",
        f"- Target Career Match: {best['target_career_match']:.2f}%",
        "",
        "Evidence to Lead With",
        "---------------------",
    ]
    if strong_skills:
        lines.extend(f"- {skill}" for skill in strong_skills)
    else:
        lines.append("- No strong-evidence skills were identified.")

    lines.extend(["", "Matched Requirements", "--------------------"])
    if matched_skills:
        lines.extend(f"- {skill}" for skill in matched_skills)
    else:
        lines.append("- No required skills are currently matched.")

    lines.extend(["", "Remaining Gaps", "--------------"])
    if remaining_gaps:
        lines.extend(f"- {skill}" for skill in remaining_gaps)
    else:
        lines.append("- No required-skill gaps remain under the current rules.")

    lines.extend(
        [
            "",
            "Application Checklist",
            "---------------------",
            "1. Load the selected saved analysis in TalentBridge.",
            "2. Tailor the resume to the posting using only truthful, "
            "supportable evidence.",
            "3. Lead with the strongest evidence listed above and add "
            "measurable scope only when it is accurate.",
            (
                "4. Address or honestly disclose every remaining gap before "
                "presenting the resume as a complete match."
                if remaining_gaps
                else
                "4. Recheck the original posting for non-skill requirements "
                "before applying."
            ),
            "5. Verify dates, contact details, eligibility, experience years, "
            "and every critical requirement against the original posting.",
            "6. Prepare examples and portfolio proof that you can explain in "
            "an interview.",
            "",
            f"Why This Version: {best['reason']}",
            f"Recommended Use: {best['recommendation']}",
            "",
            "Important",
            "---------",
            "This plan ranks comparable saved resume evidence under the "
            "current TalentBridge rules. It does not include private resume "
            "text, verify proficiency or eligibility, predict an employer "
            "decision, or guarantee an interview. Never add a skill, result, "
            "project, or experience you cannot truthfully explain and prove.",
            "",
        ]
    )
    return "\n".join(lines)


def generate_saved_progress_insight(progress_group):
    """Explain the direction of one comparable saved-analysis history."""
    if not progress_group:
        raise ValueError("Choose a comparable saved-analysis history first.")

    positive_metrics = []
    negative_metrics = []
    unchanged_metrics = []
    for metric in progress_group.get("metric_rows", []):
        label = str(metric.get("Metric", "Score"))
        raw_delta = metric.get("delta_value")
        if raw_delta is None:
            delta_match = re.search(
                r"[-+]?\d+(?:\.\d+)?",
                str(metric.get("Change", "0")),
            )
            raw_delta = delta_match.group(0) if delta_match else 0
        try:
            delta = float(raw_delta)
        except (TypeError, ValueError):
            delta = 0.0

        if delta > 0.005:
            positive_metrics.append(label)
        elif delta < -0.005:
            negative_metrics.append(label)
        else:
            unchanged_metrics.append(label)

    skills_gained = list(progress_group.get("skills_gained", []))
    skills_lost = list(progress_group.get("skills_no_longer_matched", []))
    remaining_gaps = list(progress_group.get("remaining_gaps", []))

    if positive_metrics and negative_metrics:
        status = "Mixed Progress"
        summary = (
            f"{len(positive_metrics)} score(s) improved while "
            f"{len(negative_metrics)} declined. Review the changed résumé "
            "evidence before treating this as overall progress."
        )
    elif negative_metrics:
        status = "Needs Attention"
        summary = (
            f"{len(negative_metrics)} score(s) declined across the saved "
            "history. Check whether required-skill evidence was removed or "
            "weakened."
        )
    elif positive_metrics:
        status = "Progress Detected"
        summary = (
            f"{len(positive_metrics)} score(s) improved across the comparable "
            "saved analyses."
        )
    elif skills_gained or skills_lost:
        status = "Evidence Changed"
        summary = (
            "Required-skill evidence changed, although the four headline "
            "scores did not move measurably."
        )
    else:
        status = "No Measurable Change"
        summary = (
            "No measurable score or required-skill change appears across "
            "these comparable analyses."
        )

    if remaining_gaps:
        priority_gaps = remaining_gaps[:3]
        next_step = (
            "Strengthen truthful résumé evidence for "
            f"{', '.join(priority_gaps)}, then analyze this same job again."
        )
    elif skills_lost:
        next_step = (
            "Review the evidence for skills that are no longer matched, then "
            "reanalyze this same job."
        )
    else:
        next_step = (
            "Maintain the current evidence and add measurable scope or results "
            "only when they are truthful and supportable."
        )

    return {
        "status": status,
        "summary": summary,
        "next_step": next_step,
        "positive_metrics": positive_metrics,
        "negative_metrics": negative_metrics,
        "unchanged_metrics": unchanged_metrics,
        "skills_gained": skills_gained,
        "skills_no_longer_matched": skills_lost,
        "remaining_gaps": remaining_gaps,
        "disclaimer": (
            "This insight describes changes in saved résumé evidence under "
            "the current TalentBridge rules. It does not verify completed "
            "training, proficiency, or an employer decision."
        ),
    }


def generate_saved_progress_report(progress_group, target_career):
    """Create a portable text summary for one comparable progress history."""
    if not progress_group:
        raise ValueError("Choose a comparable saved-analysis history first.")

    earliest = progress_group.get("earliest", {})
    latest = progress_group.get("latest", {})
    analysis_count = int(progress_group.get("analysis_count", 0) or 0)
    job_title = str(progress_group.get("job_title", "") or "Saved Job")
    start_date = str(earliest.get("created_at", ""))[:10] or "Unknown"
    end_date = str(latest.get("created_at", ""))[:10] or "Unknown"

    lines = [
        "TalentBridge AI - Saved Analysis Progress Report",
        "================================================",
        "",
        f"Target Career: {target_career or 'Not specified'}",
        f"Job: {job_title}",
        f"Comparable Analyses: {analysis_count}",
        f"Progress Period: {start_date} to {end_date}",
        "",
        "Score Progress",
        "--------------",
    ]

    metric_rows = progress_group.get("metric_rows", [])
    if metric_rows:
        for metric in metric_rows:
            lines.append(
                f"- {metric.get('Metric', 'Score')}: "
                f"{metric.get('Earliest', 'Not available')} -> "
                f"{metric.get('Latest', 'Not available')} "
                f"({metric.get('Change', 'No change reported')})"
            )
    else:
        lines.append("- No score history is available.")

    insight = generate_saved_progress_insight(progress_group)
    best_version = select_best_saved_resume_version(progress_group)
    lines.extend(
        [
            "",
            "Progress Insight",
            "----------------",
            f"Status: {insight['status']}",
            insight["summary"],
            f"Recommended Next Step: {insight['next_step']}",
            "",
            "Best Saved Resume Version",
            "-------------------------",
            f"Saved Date: {best_version['saved_date']}",
            (
                "Evidence-Adjusted Score: "
                f"{best_version['evidence_adjusted_score']:.2f}%"
            ),
            (
                "Job Description Match: "
                f"{best_version['job_description_match']:.2f}%"
            ),
            f"Semantic Match: {best_version['semantic_match']:.2f}%",
            (
                "Target Career Match: "
                f"{best_version['target_career_match']:.2f}%"
            ),
            "Strongest Evidence: "
            + (
                ", ".join(best_version["strong_skills"])
                if best_version["strong_skills"]
                else "No strong-evidence skills identified"
            ),
            "Remaining Gaps: "
            + (
                ", ".join(best_version["remaining_gaps"])
                if best_version["remaining_gaps"]
                else "None"
            ),
            f"Why Selected: {best_version['reason']}",
            f"Recommended Use: {best_version['recommendation']}",
        ]
    )

    skill_sections = (
        ("Skills Gained", progress_group.get("skills_gained", []),
         "No newly matched skills."),
        ("No Longer Matched", progress_group.get("skills_no_longer_matched", []),
         "No matched skills were lost."),
        ("Remaining Gaps", progress_group.get("remaining_gaps", []),
         "No required-skill gaps remain."),
    )
    for heading, skills, empty_message in skill_sections:
        lines.extend(["", heading, "-" * len(heading)])
        if skills:
            lines.extend(f"- {skill}" for skill in skills)
        else:
            lines.append(f"- {empty_message}")

    lines.extend(
        [
            "",
            "Important",
            "---------",
            "This report re-evaluates private saved inputs with the current "
            "TalentBridge rules. It measures resume-evidence changes for the "
            "same job posting; it does not verify skill growth, predict an "
            "employer decision, or guarantee an interview.",
            "",
        ]
    )
    return "\n".join(lines)


def generate_score_interpretation(
    job_comparison,
    semantic_match_details,
    target_career_match,
):
    """Explain why the three public match scores can legitimately differ."""
    matched_skills = job_comparison.get("matched_skills", [])
    missing_skills = job_comparison.get("missing_skills", [])
    required_count = len(matched_skills) + len(missing_skills)
    job_score = float(job_comparison.get("match_score", 0) or 0)

    semantic_match_details = semantic_match_details or {}
    semantic_score = float(
        semantic_match_details.get("semantic_score", 0) or 0
    )
    context_score = float(
        semantic_match_details.get("context_similarity_score", 0) or 0
    )
    skill_alignment_score = float(
        semantic_match_details.get("skill_alignment_score", 0) or 0
    )
    preferred_count = int(
        semantic_match_details.get("preferred_skill_count", 0) or 0
    )

    target_career_match = target_career_match or {}
    target_score = float(target_career_match.get("match_score", 0) or 0)
    target_career = target_career_match.get("target_career", "selected career")
    target_status = target_career_match.get("status", "Not available")

    if required_count:
        job_reason = (
            f"Matched {len(matched_skills)} of {required_count} required "
            "skills."
        )
    else:
        job_reason = "No recognizable required skills were detected."
    if preferred_count:
        job_reason += (
            f" {preferred_count} preferred skill(s) are reported separately."
        )

    if required_count:
        semantic_reason = (
            f"Combines 65% required-skill alignment "
            f"({skill_alignment_score:.2f}%) and 35% résumé/job context "
            f"similarity ({context_score:.2f}%)."
        )
    else:
        semantic_reason = (
            f"Uses résumé/job context similarity ({context_score:.2f}%) "
            "because no recognizable required skills were detected."
        )

    target_reason = (
        f"Measures the résumé against the broader {target_career} benchmark, "
        f"not only this posting. Current status: {target_status}."
    )

    score_rows = [
        {
            "Score": "Job Description Match",
            "Result": f"{job_score:.2f}%",
            "What It Measures": "Required skills in this posting",
            "Why This Result": job_reason,
        },
        {
            "Score": "Semantic Match",
            "Result": f"{semantic_score:.2f}%",
            "What It Measures": "Required skills plus wording and context",
            "Why This Result": semantic_reason,
        },
        {
            "Score": "Target Career Match",
            "Result": f"{target_score:.2f}%",
            "What It Measures": f"Broader {target_career} readiness",
            "Why This Result": target_reason,
        },
    ]

    if required_count == 0:
        summary = (
            "The posting lacks recognizable required skills, so the scores "
            "should not be treated as a complete comparison."
        )
        next_step = (
            "Paste the complete job responsibilities and required qualifications."
        )
    elif job_score - semantic_score >= 10:
        summary = (
            "Required-skill coverage is stronger than résumé/job wording and "
            "context alignment."
        )
        next_step = (
            "Tailor truthful résumé bullets to the posting's responsibilities "
            "and terminology while keeping the proven skills unchanged."
        )
    elif semantic_score - job_score >= 10:
        summary = (
            "Résumé/job wording and context are stronger than exact required-"
            "skill coverage."
        )
        next_step = (
            "Review the missing required skills and add them only when supported "
            "by truthful evidence."
        )
    elif abs(job_score - semantic_score) < 10:
        summary = (
            "Required-skill coverage and résumé/job context tell a consistent "
            "story."
        )
        next_step = (
            "Prepare evidence-based examples for the matched requirements and "
            "verify every résumé claim."
        )
    else:
        summary = "The scores use different evidence and should be read separately."
        next_step = "Review the detailed evidence below each score."

    if target_score + 10 <= job_score:
        summary += (
            f" This posting fits better than the broader {target_career} benchmark."
        )
    elif target_score >= job_score + 10:
        summary += (
            f" Broader {target_career} readiness is stronger than the fit for "
            "this specific posting."
        )

    return {
        "scores": score_rows,
        "summary": summary,
        "next_step": next_step,
        "disclaimer": (
            "These scores answer different questions. They are guidance, not "
            "a hiring decision or guarantee."
        ),
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


_BETA_TEST_PLANS = {
    "Job Seeker": {
        "objective": (
            "Confirm that a job seeker can reuse private inputs, understand the "
            "evidence-based results, and leave with a practical next action."
        ),
        "scenarios": [
            {
                "id": "reuse_private_inputs",
                "title": "Reuse private inputs",
                "instructions": (
                    "Load a saved resume and saved job description, or save and "
                    "reload new test inputs."
                ),
                "expected_result": (
                    "The selected inputs return to the comparison form without "
                    "copying and pasting them again."
                ),
            },
            {
                "id": "review_job_match",
                "title": "Review a job match",
                "instructions": (
                    "Run a comparison and inspect the scores, required skills, "
                    "evidence, and remaining gaps."
                ),
                "expected_result": (
                    "The result explains what each score measures and connects "
                    "every recommendation to visible resume evidence."
                ),
            },
            {
                "id": "change_target_career",
                "title": "Change the target career",
                "instructions": (
                    "Choose a different target career in the sidebar while keeping "
                    "the same resume and job description."
                ),
                "expected_result": (
                    "Target Career Match and career-readiness guidance update for "
                    "the new career."
                ),
            },
            {
                "id": "use_next_action",
                "title": "Use a next action",
                "instructions": (
                    "Review the improvement, learning, interview, or application "
                    "plan and download one report."
                ),
                "expected_result": (
                    "The user can identify a truthful next step and download a "
                    "report without exposing full private inputs."
                ),
            },
        ],
    },
    "HR / Recruiter": {
        "objective": (
            "Confirm that an HR reviewer can compare candidates consistently while "
            "keeping evidence strength and human review visible."
        ),
        "scenarios": [
            {
                "id": "review_candidate_fit",
                "title": "Review candidate fit",
                "instructions": (
                    "Compare a candidate resume with a job description and inspect "
                    "required, preferred, and critical requirements."
                ),
                "expected_result": (
                    "Required and preferred skills are separated, and uncertain or "
                    "missing evidence is not presented as proven."
                ),
            },
            {
                "id": "trace_evidence",
                "title": "Trace the evidence",
                "instructions": (
                    "Open evidence traceability and requirement-evidence strength."
                ),
                "expected_result": (
                    "Each supported requirement includes a resume excerpt and a "
                    "plain-language evidence-strength explanation."
                ),
            },
            {
                "id": "screen_candidates",
                "title": "Screen multiple candidates",
                "instructions": (
                    "Use HR Batch Screening with at least two fictional or consented "
                    "candidate resumes."
                ),
                "expected_result": (
                    "Candidates are ranked consistently and gaps remain visible for "
                    "human review."
                ),
            },
            {
                "id": "download_hr_report",
                "title": "Download the HR report",
                "instructions": "Download and inspect the recruiter-ready report.",
                "expected_result": (
                    "The report contains evidence-based guidance and states that it "
                    "is not an employer decision."
                ),
            },
        ],
    },
    "Training Center": {
        "objective": (
            "Confirm that a training provider can turn evidence-based skill gaps "
            "into a clear, measurable learning pathway."
        ),
        "scenarios": [
            {
                "id": "review_learner_readiness",
                "title": "Review learner readiness",
                "instructions": (
                    "Analyze a fictional or consented learner resume against a "
                    "target role."
                ),
                "expected_result": (
                    "The app separates current evidence, missing skills, and skills "
                    "that need stronger proof."
                ),
            },
            {
                "id": "prioritize_training",
                "title": "Prioritize training",
                "instructions": (
                    "Review the skill-gap priorities and personalized course plan."
                ),
                "expected_result": (
                    "The highest-value gaps appear first with concrete learning "
                    "tasks."
                ),
            },
            {
                "id": "track_portfolio_progress",
                "title": "Track portfolio progress",
                "instructions": (
                    "Add test portfolio links and progress statuses for missing "
                    "skills, then generate the evidence summary."
                ),
                "expected_result": (
                    "Progress and portfolio evidence affect the proof-based view "
                    "without claiming verified proficiency."
                ),
            },
            {
                "id": "download_training_report",
                "title": "Download the training report",
                "instructions": "Download and inspect the Training Center report.",
                "expected_result": (
                    "The report gives an actionable learning pathway and retains the "
                    "evidence-use disclaimer."
                ),
            },
        ],
    },
}


def build_beta_test_plan(user_mode):
    """Return a role-specific, privacy-safe beta test plan."""
    if user_mode not in _BETA_TEST_PLANS:
        raise ValueError("Unsupported beta tester role.")

    source_plan = _BETA_TEST_PLANS[user_mode]
    scenarios = [dict(scenario) for scenario in source_plan["scenarios"]]
    return {
        "user_mode": user_mode,
        "objective": source_plan["objective"],
        "scenarios": scenarios,
        "scenario_count": len(scenarios),
        "success_criteria": (
            "Complete every scenario, give an average rating of at least 4 out of "
            "5, and report no major or blocker issue."
        ),
        "privacy_note": (
            "Use fictional, public, or consented test data. Do not enter names, "
            "email addresses, secrets, or confidential resume content in feedback."
        ),
    }


def _clean_beta_feedback_text(value, limit=2000):
    """Normalize downloadable feedback without retaining control characters."""
    cleaned = " ".join(str(value or "").replace("\x00", " ").split())
    return cleaned[:limit]


def generate_beta_feedback_report(
    user_mode,
    completed_scenario_ids=None,
    ratings=None,
    issue_severity="None",
    issue_notes="",
    improvement_suggestion="",
    tester_alias="Anonymous tester",
):
    """Summarize beta results without including resume or job-description text."""
    plan = build_beta_test_plan(user_mode)
    valid_ids = {scenario["id"] for scenario in plan["scenarios"]}
    completed_ids = {
        item for item in (completed_scenario_ids or []) if item in valid_ids
    }
    normalized_ratings = {}
    for name, value in (ratings or {}).items():
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            continue
        normalized_ratings[_clean_beta_feedback_text(name, 80)] = max(
            1.0, min(5.0, numeric_value)
        )

    completed_count = len(completed_ids)
    scenario_count = plan["scenario_count"]
    completion_rate = round((completed_count / scenario_count) * 100, 2)
    average_rating = (
        round(sum(normalized_ratings.values()) / len(normalized_ratings), 2)
        if normalized_ratings
        else 0.0
    )
    allowed_severities = {"None", "Minor", "Major", "Blocker"}
    severity = issue_severity if issue_severity in allowed_severities else "None"

    if severity == "Blocker":
        status = "Blocked"
        next_action = "Resolve the blocker and repeat the affected scenarios."
    elif severity == "Major" or completion_rate < 100 or average_rating < 4:
        status = "Needs Review"
        next_action = (
            "Review the incomplete or low-rated areas, address major issues, and "
            "run another beta session."
        )
    else:
        status = "Passed"
        next_action = (
            "Record the successful session and continue collecting feedback from "
            "another tester role."
        )

    completed_titles = [
        scenario["title"]
        for scenario in plan["scenarios"]
        if scenario["id"] in completed_ids
    ]
    incomplete_titles = [
        scenario["title"]
        for scenario in plan["scenarios"]
        if scenario["id"] not in completed_ids
    ]
    rating_lines = [
        f"- {name}: {value:.1f}/5"
        for name, value in normalized_ratings.items()
    ] or ["- No ratings recorded."]

    report_lines = [
        "TalentBridge AI - Beta Feedback Report",
        "======================================",
        "",
        f"Tester Role: {user_mode}",
        f"Tester Alias: {_clean_beta_feedback_text(tester_alias, 100) or 'Anonymous tester'}",
        f"Beta Status: {status}",
        f"Scenarios Completed: {completed_count} of {scenario_count} ({completion_rate:.2f}%)",
        f"Average Rating: {average_rating:.2f}/5",
        f"Highest Issue Severity: {severity}",
        "",
        "Completed Scenarios",
        "-------------------",
        *([f"- {title}" for title in completed_titles] or ["- None"]),
        "",
        "Incomplete Scenarios",
        "--------------------",
        *([f"- {title}" for title in incomplete_titles] or ["- None"]),
        "",
        "Ratings",
        "-------",
        *rating_lines,
        "",
        "Issue Notes",
        "-----------",
        _clean_beta_feedback_text(issue_notes) or "No issue notes recorded.",
        "",
        "Improvement Suggestion",
        "----------------------",
        _clean_beta_feedback_text(improvement_suggestion)
        or "No improvement suggestion recorded.",
        "",
        "Recommended Next Action",
        "-----------------------",
        next_action,
        "",
        "Privacy and Scope",
        "-----------------",
        (
            "This summary intentionally excludes resume and job-description text. "
            "Beta feedback measures user experience; it does not verify score "
            "accuracy, make an employer decision, or guarantee an interview."
        ),
    ]

    return {
        "status": status,
        "completed_count": completed_count,
        "scenario_count": scenario_count,
        "completion_rate": completion_rate,
        "average_rating": average_rating,
        "issue_severity": severity,
        "next_action": next_action,
        "report_text": "\n".join(report_lines),
    }
