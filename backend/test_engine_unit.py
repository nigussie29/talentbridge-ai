import unittest

from career_engine import (
    analyze_career_profile,
    analyze_job_description,
    analyze_resume_text,
    analyze_skill_confidence,
    calculate_proof_based_readiness_score,
    calculate_semantic_match_details,
    calculate_semantic_match_score,
    calculate_target_career_match,
    compare_resume_to_job,
    generate_interview_readiness_report,
    generate_interview_preparation_plan,
    generate_progress_tracker,
    generate_resume_improvement_plan,
    rank_career_matches,
    recommend_careers_from_resume,
)


class TalentBridgeEngineTests(unittest.TestCase):
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
        self.assertEqual(len(result["rankings"]), 4)
        self.assertEqual(
            [item["rank"] for item in result["rankings"]],
            [1, 2, 3, 4],
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
