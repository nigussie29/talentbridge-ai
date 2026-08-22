import unittest

from career_engine import (
    analyze_career_profile,
    analyze_job_description,
    analyze_resume_text,
    analyze_skill_confidence,
    calculate_analysis_confidence,
    calculate_improvement_score,
    calculate_proof_based_readiness_score,
    calculate_semantic_match_details,
    calculate_semantic_match_score,
    calculate_target_career_match,
    classify_job_skills,
    compare_resume_to_job,
    evaluate_critical_requirements,
    generate_application_decision,
    generate_interview_readiness_report,
    generate_interview_preparation_plan,
    generate_match_action_summary,
    generate_progress_tracker,
    generate_resume_improvement_plan,
    generate_score_interpretation,
    prioritize_missing_skills,
    rank_career_matches,
    recommend_careers_from_resume,
    validate_analysis_inputs,
)


class TalentBridgeEngineTests(unittest.TestCase):
    def test_analysis_confidence_is_low_for_brief_perfect_match(self):
        result = calculate_analysis_confidence(
            {
                "resume_word_count": 13,
                "job_word_count": 15,
                "resume_skill_count": 4,
                "job_skill_count": 7,
            },
            {
                "matched_skills": [
                    "Python",
                    "SQL",
                    "Machine Learning",
                    "Docker",
                ],
                "missing_skills": [],
                "match_score": 100.0,
            },
            {
                "met_count": 0,
                "unclear_count": 0,
                "missing_count": 0,
            },
        )

        self.assertEqual(result["confidence_level"], "Low")
        self.assertLess(result["confidence_score"], 60)
        self.assertIn("preliminary", result["headline"])
        self.assertGreaterEqual(len(result["limitations"]), 3)

    def test_analysis_confidence_is_high_for_complete_evidence(self):
        result = calculate_analysis_confidence(
            {
                "resume_word_count": 240,
                "job_word_count": 180,
                "resume_skill_count": 12,
                "job_skill_count": 10,
            },
            {
                "matched_skills": [
                    "Python",
                    "SQL",
                    "Machine Learning",
                    "Docker",
                    "Cloud",
                    "REST APIs",
                ],
                "missing_skills": ["Kubernetes", "Databricks"],
                "match_score": 75.0,
            },
            {
                "met_count": 3,
                "unclear_count": 0,
                "missing_count": 1,
            },
        )

        self.assertEqual(result["confidence_level"], "High")
        self.assertEqual(result["confidence_score"], 100.0)
        self.assertEqual(result["limitations"], [])
        self.assertIn("does not measure candidate quality", result["disclaimer"])

    def test_analysis_confidence_reduces_for_unclear_critical_evidence(self):
        result = calculate_analysis_confidence(
            {
                "resume_word_count": 240,
                "job_word_count": 180,
                "resume_skill_count": 12,
                "job_skill_count": 10,
            },
            {
                "matched_skills": [
                    "Python",
                    "SQL",
                    "Machine Learning",
                    "Docker",
                    "Cloud",
                    "REST APIs",
                ],
                "missing_skills": ["Kubernetes", "Databricks"],
                "match_score": 75.0,
            },
            {
                "met_count": 0,
                "unclear_count": 4,
                "missing_count": 0,
            },
        )

        self.assertEqual(result["confidence_level"], "Moderate")
        self.assertEqual(result["confidence_score"], 75.0)
        self.assertIn("4 critical requirement", result["limitations"][0])

    def test_analysis_confidence_treats_clear_missing_as_resolved(self):
        result = calculate_analysis_confidence(
            {
                "resume_word_count": 240,
                "job_word_count": 180,
                "resume_skill_count": 12,
                "job_skill_count": 10,
            },
            {
                "matched_skills": ["Python", "SQL", "Docker"],
                "missing_skills": [
                    "Kubernetes",
                    "Databricks",
                    "Apache Spark",
                    "Cloud",
                    "REST APIs",
                ],
                "match_score": 37.5,
            },
            {
                "met_count": 1,
                "unclear_count": 0,
                "missing_count": 3,
            },
        )

        self.assertEqual(result["confidence_level"], "High")
        self.assertEqual(result["confidence_score"], 100.0)

    def test_score_interpretation_explains_three_different_scores(self):
        result = generate_score_interpretation(
            {
                "matched_skills": ["Python", "SQL", "Machine Learning", "Docker"],
                "missing_skills": [],
                "match_score": 100.0,
            },
            {
                "semantic_score": 78.55,
                "context_similarity_score": 38.71,
                "skill_alignment_score": 100.0,
                "preferred_skill_count": 3,
            },
            {
                "target_career": "AI Engineer",
                "match_score": 61.9,
                "status": "Developing candidate",
            },
        )

        self.assertEqual(len(result["scores"]), 3)
        self.assertIn("4 of 4 required skills", result["scores"][0]["Why This Result"])
        self.assertIn("3 preferred", result["scores"][0]["Why This Result"])
        self.assertIn("65% required-skill alignment", result["scores"][1]["Why This Result"])
        self.assertIn("broader AI Engineer benchmark", result["scores"][2]["Why This Result"])
        self.assertIn("fits better than the broader AI Engineer", result["summary"])

    def test_score_interpretation_explains_context_boost(self):
        result = generate_score_interpretation(
            {
                "matched_skills": ["Python"],
                "missing_skills": ["SQL"],
                "match_score": 50.0,
            },
            {
                "semantic_score": 65.0,
                "context_similarity_score": 92.86,
                "skill_alignment_score": 50.0,
                "preferred_skill_count": 0,
            },
            {
                "target_career": "Data Analyst",
                "match_score": 80.0,
                "status": "Almost ready",
            },
        )

        self.assertIn("context are stronger", result["summary"])
        self.assertIn("Broader Data Analyst readiness", result["summary"])
        self.assertIn("missing required skills", result["next_step"])

    def test_score_interpretation_handles_consistent_scores(self):
        result = generate_score_interpretation(
            {
                "matched_skills": ["Python", "SQL"],
                "missing_skills": [],
                "match_score": 100.0,
            },
            {
                "semantic_score": 94.0,
                "context_similarity_score": 82.86,
                "skill_alignment_score": 100.0,
                "preferred_skill_count": 0,
            },
            {
                "target_career": "Data Analyst",
                "match_score": 94.12,
                "status": "Strong candidate",
            },
        )

        self.assertIn("consistent story", result["summary"])
        self.assertIn("evidence-based examples", result["next_step"])

    def test_score_interpretation_requires_job_information(self):
        result = generate_score_interpretation(
            {"matched_skills": [], "missing_skills": [], "match_score": 0.0},
            {
                "semantic_score": 20.0,
                "context_similarity_score": 20.0,
                "skill_alignment_score": 0.0,
                "preferred_skill_count": 0,
            },
            {
                "target_career": "AI Engineer",
                "match_score": 60.0,
                "status": "Developing candidate",
            },
        )

        self.assertIn("lacks recognizable required skills", result["summary"])
        self.assertIn("complete job responsibilities", result["next_step"])

    def test_job_skill_classifier_separates_required_and_preferred(self):
        result = classify_job_skills(
            "Required skills: Python and SQL. "
            "Kubernetes and Databricks are preferred."
        )

        self.assertEqual(result["required_skills"], ["Python", "SQL"])
        self.assertEqual(
            result["preferred_skills"],
            ["Kubernetes", "Databricks"],
        )
        self.assertEqual(
            result["classification_method"],
            "explicit_preference_markers",
        )

    def test_preferred_skills_do_not_lower_required_match(self):
        resume_skills = analyze_resume_text("Built Python and SQL pipelines.")
        requirements = classify_job_skills(
            "Python and SQL are required. Kubernetes is nice to have."
        )

        comparison = compare_resume_to_job(
            resume_skills,
            requirements["required_skills"],
        )
        semantic = calculate_semantic_match_details(
            "Built Python and SQL pipelines.",
            "Python and SQL are required. Kubernetes is nice to have.",
        )

        self.assertEqual(comparison["match_score"], 100.0)
        self.assertEqual(comparison["missing_skills"], [])
        self.assertEqual(requirements["preferred_skills"], ["Kubernetes"])
        self.assertEqual(semantic["skill_alignment_score"], 100.0)
        self.assertEqual(semantic["required_skill_count"], 2)
        self.assertEqual(semantic["preferred_skill_count"], 1)

    def test_required_classification_wins_when_skill_appears_in_both_groups(self):
        result = classify_job_skills(
            "Kubernetes is preferred. Kubernetes is required for deployment."
        )

        self.assertEqual(result["required_skills"], ["Kubernetes"])
        self.assertEqual(result["preferred_skills"], [])

    def test_job_skill_classifier_supports_preferred_sections(self):
        result = classify_job_skills(
            "Requirements:\nPython and SQL\n"
            "Preferred Qualifications:\nDocker and Kubernetes"
        )

        self.assertEqual(result["required_skills"], ["Python", "SQL"])
        self.assertEqual(
            result["preferred_skills"],
            ["Docker", "Kubernetes"],
        )

    def test_unmarked_job_skills_remain_required_for_compatibility(self):
        result = classify_job_skills(
            "Seeking a data analyst with Python, SQL, Power BI, and Excel."
        )

        self.assertEqual(
            result["required_skills"],
            ["Python", "SQL", "Power BI", "Excel"],
        )
        self.assertEqual(result["preferred_skills"], [])
        self.assertEqual(
            result["classification_method"],
            "unmarked_skills_treated_as_required",
        )

    def test_application_decision_reports_strong_supported_match(self):
        result = generate_application_decision(
            {
                "matched_skills": ["Python", "SQL", "Cloud", "Docker"],
                "missing_skills": [],
                "match_score": 100.0,
            },
            semantic_match_score=72.0,
            critical_requirements={
                "requirements": [
                    {
                        "category": "Experience",
                        "requirement": "5+ years of experience",
                        "status": "Met",
                    },
                    {
                        "category": "Technology",
                        "requirement": "Python",
                        "status": "Met",
                    },
                ],
                "met_count": 2,
                "unclear_count": 0,
                "missing_count": 0,
            },
        )

        self.assertEqual(result["decision"], "Strong Match")
        self.assertEqual(result["message_type"], "success")
        self.assertEqual(result["critical_support_score"], 100.0)

    def test_application_decision_respects_missing_core_requirement(self):
        result = generate_application_decision(
            {
                "matched_skills": ["Python", "SQL", "Cloud", "Docker"],
                "missing_skills": ["Databricks"],
                "match_score": 80.0,
            },
            semantic_match_score=70.0,
            critical_requirements={
                "requirements": [
                    {
                        "category": "Education",
                        "requirement": "Bachelor's degree",
                        "status": "Missing",
                    },
                    {
                        "category": "Technology",
                        "requirement": "Python",
                        "status": "Met",
                    },
                ],
                "met_count": 1,
                "unclear_count": 0,
                "missing_count": 1,
            },
        )

        self.assertEqual(result["decision"], "Improve Before Applying")
        self.assertIn("Bachelor's degree", result["blocking_requirements"])
        self.assertIn("truthfully address", result["next_action"])

    def test_application_decision_handles_competitive_match_with_gaps(self):
        result = generate_application_decision(
            {
                "matched_skills": ["Python", "SQL", "Power BI"],
                "missing_skills": ["Cloud", "Docker"],
                "match_score": 60.0,
            },
            semantic_match_score=50.0,
            critical_requirements={
                "requirements": [
                    {
                        "category": "Technology",
                        "requirement": "Python",
                        "status": "Met",
                    },
                    {
                        "category": "Technology",
                        "requirement": "SQL",
                        "status": "Met",
                    },
                    {
                        "category": "Technology",
                        "requirement": "Cloud",
                        "status": "Missing",
                    },
                ],
                "met_count": 2,
                "unclear_count": 0,
                "missing_count": 1,
            },
        )

        self.assertEqual(result["decision"], "Consider Applying")
        self.assertEqual(result["message_type"], "info")

    def test_application_decision_requires_detected_job_requirements(self):
        result = generate_application_decision(
            {"matched_skills": [], "missing_skills": [], "match_score": 0.0},
            semantic_match_score=0.0,
            critical_requirements={
                "requirements": [],
                "met_count": 0,
                "unclear_count": 0,
                "missing_count": 0,
            },
        )

        self.assertEqual(result["decision"], "Insufficient Information")
        self.assertIn("complete responsibilities", result["next_action"])

    def test_critical_requirements_separate_met_and_missing_evidence(self):
        result = evaluate_critical_requirements(
            (
                "Senior QA Analyst with 10+ years of experience using Python "
                "and SQL for enterprise data validation."
            ),
            (
                "We are seeking a senior QA Analyst. 8+ years of experience "
                "with Python and SQL is required. Strong hands-on experience "
                "with Databricks is required."
            ),
        )

        requirements = {
            (item["category"], item["requirement"]): item["status"]
            for item in result["requirements"]
        }
        self.assertEqual(
            requirements[("Seniority", "Senior-level candidate")],
            "Met",
        )
        self.assertEqual(
            requirements[("Experience", "8+ years of experience with Python, SQL")],
            "Met",
        )
        self.assertEqual(requirements[("Technology", "Databricks")], "Missing")
        self.assertGreaterEqual(result["met_count"], 3)
        self.assertEqual(result["overall_status"], "Critical gaps detected")

    def test_critical_requirements_keep_leadership_duration_unclear(self):
        result = evaluate_critical_requirements(
            "Senior QA Analyst with 8+ years of experience in quality assurance.",
            "5+ years of experience leading QA efforts is required.",
        )

        experience_requirement = next(
            item
            for item in result["requirements"]
            if item["category"] == "Experience"
        )
        self.assertEqual(experience_requirement["status"], "Unclear")
        self.assertIn("leadership duration", experience_requirement["evidence"])

    def test_critical_requirements_accept_higher_degree(self):
        result = evaluate_critical_requirements(
            "Education: Master of Science degree in Applied Mathematics.",
            "A Bachelor's degree in mathematics or statistics is required.",
        )

        education_requirement = next(
            item
            for item in result["requirements"]
            if item["category"] == "Education"
        )
        self.assertEqual(education_requirement["status"], "Met")
        self.assertIn("Master's degree", education_requirement["evidence"])

    def test_critical_requirements_do_not_treat_preferences_as_mandatory(self):
        result = evaluate_critical_requirements(
            "QA Analyst with Python and SQL experience.",
            (
                "Python and SQL are required. Databricks is preferred. "
                "A Master's degree is optional."
            ),
        )

        requirement_names = {
            item["requirement"] for item in result["requirements"]
        }
        self.assertIn("Python", requirement_names)
        self.assertIn("SQL", requirement_names)
        self.assertNotIn("Databricks", requirement_names)
        self.assertNotIn("Master's degree", requirement_names)

    def test_input_quality_blocks_chat_instructions_in_job_description(self):
        result = validate_analysis_inputs(
            "Built Python and SQL data-validation projects for reporting teams.",
            (
                "Open Manage app, reboot app, then click Compare Resume to Job "
                "Description and send me a screenshot."
            ),
        )

        self.assertFalse(result["can_analyze"])
        self.assertEqual(result["quality_level"], "Blocked")
        self.assertIn("app or chat instructions", result["errors"][0])

    def test_input_quality_allows_brief_test_data_with_warning(self):
        result = validate_analysis_inputs(
            "Built Python SQL project.",
            "Seeking Python SQL and Power BI developer.",
        )

        self.assertTrue(result["can_analyze"])
        self.assertEqual(result["quality_level"], "Review Recommended")
        self.assertGreaterEqual(len(result["warnings"]), 2)

    def test_input_quality_accepts_detailed_inputs(self):
        resume = (
            "Built Python and SQL machine learning pipelines, analyzed datasets "
            "with Pandas, created Power BI dashboards, deployed FastAPI services "
            "with Docker to Azure, used Git for version control, documented model "
            "results, and presented findings to technical and business stakeholders. "
        ) * 2
        job = (
            "The engineer will build Python and SQL machine learning pipelines, "
            "analyze datasets with Pandas, create data visualizations, develop "
            "FastAPI REST APIs, package services with Docker, deploy to Azure, use "
            "Git for version control, document results, and communicate findings "
            "to technical and business stakeholders. "
        ) * 2

        result = validate_analysis_inputs(resume, job)

        self.assertTrue(result["can_analyze"])
        self.assertEqual(result["quality_level"], "Ready")
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])

    def test_match_action_summary_prioritizes_qa_gaps(self):
        summary = generate_match_action_summary(
            {
                "matched_skills": ["SQL", "Data Validation", "ETL Testing"],
                "missing_skills": [
                    "Data Engineering",
                    "Databricks",
                    "Test Automation",
                    "Git",
                ],
                "match_score": 42.86,
            },
            target_career="QA Analyst / Data Quality Analyst",
        )

        self.assertEqual(summary["fit_level"], "Low Skill Match")
        self.assertEqual(
            summary["priority_gaps"],
            ["Databricks", "Test Automation", "Data Engineering"],
        )
        self.assertIn("truthful evidence", summary["next_action"])

    def test_match_action_summary_handles_complete_match(self):
        summary = generate_match_action_summary(
            {
                "matched_skills": ["Python", "SQL"],
                "missing_skills": [],
                "match_score": 100.0,
            }
        )

        self.assertEqual(summary["fit_level"], "Strong Skill Match")
        self.assertEqual(summary["priority_gaps"], [])
        self.assertIn("interview stories", summary["next_action"])

    def test_match_action_summary_requires_job_information(self):
        summary = generate_match_action_summary(
            {"matched_skills": [], "missing_skills": [], "match_score": 0.0}
        )

        self.assertEqual(summary["fit_level"], "Insufficient Job Information")
        self.assertIn("detailed job description", summary["next_action"])

    def test_improvement_score_is_a_partial_gap_projection(self):
        result = calculate_improvement_score(
            {
                "matched_skills": [f"Matched {index}" for index in range(15)],
                "missing_skills": [f"Gap {index}" for index in range(13)],
                "match_score": 53.57,
            }
        )

        self.assertEqual(result["projected_gap_closures"], 7)
        self.assertEqual(result["estimated_score_after_training"], 78.57)
        self.assertEqual(result["improvement_potential"], 25.0)
        self.assertLess(result["estimated_score_after_training"], 100.0)
        self.assertIn("not a guaranteed result", result["projection_assumption"])

    def test_improvement_score_preserves_verified_complete_match(self):
        result = calculate_improvement_score(
            {
                "matched_skills": ["Python", "SQL"],
                "missing_skills": [],
                "match_score": 100.0,
            }
        )

        self.assertEqual(result["estimated_score_after_training"], 100.0)
        self.assertEqual(result["improvement_potential"], 0.0)

    def test_career_profile_recommends_projects_for_every_skill_gap(self):
        profile = {
            "python_skill": 4,
            "math_skill": 5,
            "data_skill": 4,
            "ai_skill": 3,
            "communication_skill": 4,
        }

        result = analyze_career_profile(profile, "AI Engineer")

        self.assertEqual(result["skill_gaps"], {"python_skill": 1, "ai_skill": 2})
        self.assertEqual(
            set(result["recommended_projects"]),
            {"python_skill", "ai_skill"},
        )

    def test_career_profile_returns_result_when_there_are_no_gaps(self):
        profile = {
            "python_skill": 5,
            "math_skill": 5,
            "data_skill": 5,
            "ai_skill": 5,
            "communication_skill": 5,
        }

        result = analyze_career_profile(profile, "AI Engineer")

        self.assertEqual(result["skill_gaps"], {})
        self.assertEqual(result["recommended_projects"], {})
        self.assertEqual(result["readiness_score"], 100.0)

    def test_resume_career_recommendation_ranks_best_fit_first(self):
        resume = (
            "Built PowerBI dashboards using PostgreSQL and Python 3. "
            "Trained scikit-learn models, deployed Docker RESTful APIs to AWS, "
            "and presented findings to stakeholders."
        )

        result = recommend_careers_from_resume(resume)

        self.assertEqual(result["recommended_career"], "Data Analyst")
        self.assertEqual(result["recommended_score"], 94.12)
        self.assertEqual(len(result["rankings"]), 5)
        self.assertEqual(
            [item["rank"] for item in result["rankings"]],
            [1, 2, 3, 4, 5],
        )
        self.assertEqual(
            result["rankings"][0]["skill_gaps"],
            {"data_skill": 1},
        )

    def test_resume_career_recommendation_requires_detected_evidence(self):
        result = recommend_careers_from_resume(
            "Reliable professional seeking a new opportunity."
        )

        self.assertIsNone(result["recommended_career"])
        self.assertEqual(result["rankings"], [])

    def test_career_ranking_is_sorted_by_fit_score(self):
        profile = {
            "python_skill": 5,
            "math_skill": 4,
            "data_skill": 5,
            "ai_skill": 2,
            "communication_skill": 4,
        }

        rankings = rank_career_matches(profile)

        scores = [item["fit_score"] for item in rankings]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertEqual(rankings[0]["career"], "Data Analyst")

    def test_same_resume_profile_recalculates_for_each_target_career(self):
        profile = {
            "python_skill": 3,
            "math_skill": 3,
            "data_skill": 4,
            "ai_skill": 3,
            "communication_skill": 4,
        }

        data_analyst = analyze_career_profile(profile, "Data Analyst")
        ai_engineer = analyze_career_profile(profile, "AI Engineer")

        self.assertEqual(data_analyst["readiness_score"], 94.12)
        self.assertEqual(ai_engineer["readiness_score"], 76.19)
        self.assertNotEqual(
            data_analyst["skill_gaps"],
            ai_engineer["skill_gaps"],
        )

    def test_target_career_match_changes_with_selected_career(self):
        detected_skills = analyze_resume_text(
            "Built PowerBI dashboards using PostgreSQL and Python. "
            "Trained machine learning models and presented to stakeholders."
        )

        data_analyst = calculate_target_career_match(
            detected_skills,
            "Data Analyst",
        )
        ai_engineer = calculate_target_career_match(
            detected_skills,
            "AI Engineer",
        )

        self.assertEqual(data_analyst["match_score"], 94.12)
        self.assertEqual(ai_engineer["match_score"], 76.19)
        self.assertEqual(data_analyst["target_career"], "Data Analyst")
        self.assertEqual(ai_engineer["target_career"], "AI Engineer")

    def test_target_career_match_requires_resume_evidence(self):
        result = calculate_target_career_match([], "Data Analyst")

        self.assertEqual(result["match_score"], 0.0)
        self.assertEqual(result["status"], "No resume evidence detected")

    def test_qa_job_description_detects_testing_requirements(self):
        skills = analyze_job_description(
            "Senior QA Analyst will create test plans and test cases, perform "
            "manual, automated, functional, regression, integration, system, performance, "
            "and user acceptance testing, track defects and requirements traceability, "
            "validate ETL source-to-target mappings, and test REST APIs with Postman. "
            "Requires Databricks, Spark SQL, PySpark, Python, Pandas, and SQL."
        )

        expected = {
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
            "Python",
            "Pandas",
            "SQL",
        }
        self.assertTrue(expected.issubset(set(skills)))

    def test_testing_mode_requires_local_testing_context(self):
        skills = analyze_resume_text(
            "Supported user acceptance testing. Built dashboards used to "
            "analyze operational performance."
        )

        self.assertIn("User Acceptance Testing", skills)
        self.assertNotIn("Performance Testing", skills)

    def test_qa_target_match_uses_qa_specific_benchmark(self):
        detected_skills = analyze_resume_text(
            "QA Analyst developed test plans and test cases, performed data "
            "validation, ETL testing, functional, regression, integration, and "
            "user acceptance testing, tracked defects, and wrote SQL queries."
        )

        result = calculate_target_career_match(
            detected_skills,
            "QA Analyst / Data Quality Analyst",
        )

        self.assertEqual(result["match_score"], 100.0)
        self.assertEqual(result["skill_gaps"], {})

    def test_qa_missing_platform_skills_are_high_priority(self):
        report = prioritize_missing_skills(
            ["REST APIs", "Apache Spark", "Databricks"],
            target_career="QA Analyst / Data Quality Analyst",
        )

        self.assertEqual(
            [item["Priority Level"] for item in report],
            ["High Priority", "High Priority", "High Priority"],
        )

    def test_resume_improvement_plan_targets_missing_job_skills(self):
        resume = (
            "Built PowerBI dashboards using PostgreSQL and Python 3. "
            "Trained scikit-learn models, deployed Docker RESTful APIs to AWS, "
            "and presented findings to stakeholders."
        )
        job_skills = analyze_job_description(
            "Python, SQL Server, Power-BI, MS Excel, Azure, machine learning, "
            "Docker, Kubernetes, REST APIs, and stakeholder communication."
        )

        plan = generate_resume_improvement_plan(resume, job_skills)

        missing_actions = [
            item for item in plan["actions"]
            if item["Current Evidence"] == "Missing"
        ]
        self.assertEqual(plan["required_skill_count"], 10)
        self.assertEqual(plan["matched_skill_count"], 8)
        self.assertEqual(plan["missing_skill_count"], 2)
        self.assertEqual(
            [item["Skill"] for item in missing_actions],
            ["Excel", "Kubernetes"],
        )
        self.assertIn("Never invent", plan["truthfulness_note"])

    def test_resume_improvement_plan_identifies_weak_evidence(self):
        plan = generate_resume_improvement_plan(
            "Currently learning Python and exploring SQL.",
            ["Python", "SQL"],
        )

        self.assertEqual(plan["missing_skill_count"], 0)
        self.assertEqual(plan["needs_stronger_evidence_count"], 2)
        self.assertTrue(
            all(item["Current Evidence"] == "Weak Evidence" for item in plan["actions"])
        )

    def test_resume_improvement_plan_handles_no_job_requirements(self):
        plan = generate_resume_improvement_plan("Built a Python project.", [])

        self.assertEqual(plan["required_skill_count"], 0)
        self.assertEqual(plan["actions"], [])
        self.assertEqual(plan["status"], "No job requirements detected.")

    def test_interview_plan_prioritizes_missing_skills_truthfully(self):
        resume = (
            "Built PowerBI dashboards using PostgreSQL and Python 3. "
            "Trained scikit-learn models, deployed Docker RESTful APIs to AWS, "
            "and presented findings to stakeholders."
        )
        job_skills = analyze_job_description(
            "Python, SQL Server, Power-BI, MS Excel, Azure, machine learning, "
            "Docker, Kubernetes, REST APIs, and stakeholder communication."
        )

        plan = generate_interview_preparation_plan(resume, job_skills)
        high_priority = [
            item for item in plan["technical_questions"]
            if item["Priority"] == "High"
        ]

        self.assertEqual(plan["technical_question_count"], 10)
        self.assertEqual(plan["behavioral_question_count"], 4)
        self.assertEqual(plan["high_priority_question_count"], 2)
        self.assertEqual(plan["missing_skill_count"], 2)
        self.assertEqual(
            [item["Skill"] for item in high_priority],
            ["Excel", "Kubernetes"],
        )
        self.assertTrue(
            all(item["Resume Evidence"] == "Missing" for item in high_priority)
        )
        self.assertIn("Never invent", plan["truthfulness_note"])

    def test_interview_plan_uses_star_and_proof_for_supported_skills(self):
        plan = generate_interview_preparation_plan(
            "Built a Python reporting tool for a real project.",
            ["Python"],
        )

        question = plan["technical_questions"][0]
        self.assertEqual(question["Priority"], "Practice")
        self.assertEqual(question["Resume Evidence"], "Strong Evidence")
        self.assertIn("Situation", question["Answer Structure"])
        self.assertIn("Proof", question["Answer Structure"])

    def test_interview_plan_handles_no_job_requirements(self):
        plan = generate_interview_preparation_plan(
            "Built a Python project.",
            [],
        )

        self.assertEqual(plan["technical_question_count"], 0)
        self.assertEqual(plan["behavioral_question_count"], 0)
        self.assertEqual(plan["technical_questions"], [])
        self.assertEqual(plan["status"], "No job requirements detected.")

    def test_resume_and_job_matching(self):
        resume_skills = analyze_resume_text("Built dashboards using Python, SQL, and Power BI.")
        job_skills = analyze_job_description(
            "Seeking a data analyst with Python, SQL, Power BI, Excel, and Git."
        )

        result = compare_resume_to_job(resume_skills, job_skills)

        self.assertEqual(result["matched_skills"], ["Python", "SQL", "Power BI"])
        self.assertEqual(result["missing_skills"], ["Excel", "Git"])
        self.assertEqual(result["match_score"], 60.0)

    def test_skill_detector_normalizes_common_tool_variations(self):
        skills = analyze_resume_text(
            "Built PowerBI reports with MS Excel and PostgreSQL. "
            "Trained scikit-learn models, used GitHub Actions and AWS, "
            "then deployed Docker services with RESTful APIs."
        )

        self.assertEqual(
            skills,
            [
                "SQL",
                "Power BI",
                "Excel",
                "Git",
                "Cloud",
                "Machine Learning",
                "REST APIs",
                "Docker",
            ],
        )

    def test_resume_and_job_detectors_share_the_same_taxonomy(self):
        text = (
            "Python 3, Power-BI, Microsoft Azure, PyTorch, Kubernetes, "
            "Databricks, and TypeScript"
        )

        self.assertEqual(analyze_resume_text(text), analyze_job_description(text))

    def test_skill_detector_uses_word_boundaries_to_avoid_false_matches(self):
        skills = analyze_job_description(
            "Digital marketing, capital planning, meaningful stories, "
            "and long-term commitment are important."
        )

        self.assertNotIn("Git", skills)
        self.assertNotIn("FastAPI", skills)
        self.assertNotIn("Statistics", skills)

    def test_skill_detector_handles_empty_input(self):
        self.assertEqual(analyze_resume_text(""), [])
        self.assertEqual(analyze_job_description(None), [])

    def test_skill_detector_recognizes_data_analysis_action_evidence(self):
        text = "Used Excel to validate records and analyzed large datasets."
        skills = analyze_resume_text(text)
        confidence = analyze_skill_confidence(text, skills)
        data_analysis = next(
            row for row in confidence if row["Skill"] == "Data Analysis"
        )

        self.assertIn("Data Analysis", skills)
        self.assertEqual(data_analysis["Confidence Level"], "Strong Evidence")

    def test_skill_confidence_uses_normalized_aliases(self):
        text = "Developed a PowerBI dashboard and presented it to executives."
        detected = analyze_resume_text(text)

        confidence = analyze_skill_confidence(text, detected)
        power_bi = next(row for row in confidence if row["Skill"] == "Power BI")

        self.assertEqual(power_bi["Confidence Level"], "Strong Evidence")

    def test_progress_tracker_handles_known_and_unknown_skills(self):
        tracker = generate_progress_tracker(["Python", "Leadership"])

        self.assertEqual(len(tracker), 2)
        self.assertEqual(tracker[0]["Status"], "Not Started")
        self.assertIn("Python project", tracker[0]["Learning Task"])
        self.assertIn("Leadership", tracker[1]["Learning Task"])

    def test_semantic_match_is_bounded_and_identical_text_scores_high(self):
        score = calculate_semantic_match_score(
            "Python SQL data analysis dashboard",
            "Python SQL data analysis dashboard",
        )

        self.assertGreaterEqual(score, 99.0)
        self.assertLessEqual(score, 100.0)

    def test_semantic_match_combines_context_and_normalized_skill_alignment(self):
        resume = (
            "Built PowerBI dashboards using PostgreSQL and Python 3. "
            "Trained scikit-learn models, deployed Docker RESTful APIs to AWS, "
            "and presented findings to stakeholders."
        )
        job_description = (
            "Seeking a data professional with Python, SQL Server, Power-BI, "
            "MS Excel, Azure, machine learning, Docker, Kubernetes, and REST APIs. "
            "Strong stakeholder communication required."
        )

        details = calculate_semantic_match_details(resume, job_description)

        self.assertEqual(details["skill_alignment_score"], 80.0)
        self.assertEqual(details["matched_required_skill_count"], 8)
        self.assertEqual(details["required_skill_count"], 10)
        self.assertGreater(details["semantic_score"], 60.0)
        self.assertLess(details["semantic_score"], 80.0)

    def test_semantic_match_handles_empty_and_stop_word_only_inputs(self):
        self.assertEqual(calculate_semantic_match_score("", "Python developer"), 0.0)
        self.assertEqual(calculate_semantic_match_score("the and", "or the"), 0.0)

    def test_semantic_match_uses_context_only_when_no_skills_are_required(self):
        details = calculate_semantic_match_details(
            "Managed regional operations and customer support.",
            "Seeking regional operations and customer support experience.",
        )

        self.assertEqual(details["scoring_method"], "context_only")
        self.assertEqual(details["required_skill_count"], 0)
        self.assertEqual(
            details["semantic_score"],
            details["context_similarity_score"],
        )

    def test_proof_based_readiness_uses_evidence_and_progress(self):
        result = calculate_proof_based_readiness_score(
            job_match_score=80,
            semantic_match_score=70,
            evidence_links={"Python": "https://github.com/example/project", "SQL": ""},
            progress_statuses={"Python": "Completed", "SQL": "In Progress"},
        )

        self.assertEqual(result["portfolio_evidence_score"], 50.0)
        self.assertEqual(result["progress_completion_score"], 50.0)
        self.assertEqual(result["proof_based_score"], 66.0)
        self.assertEqual(result["readiness_level"], "Developing Proof")

    def test_interview_readiness_decision(self):
        result = generate_interview_readiness_report(
            candidate_name="Demo Candidate",
            job_match_score=90,
            semantic_match_score=85,
            missing_skills=[],
        )

        self.assertEqual(result["decision"], "Interview Ready")
        self.assertEqual(result["missing_skills"], "No major missing skills detected.")


if __name__ == "__main__":
    unittest.main()
