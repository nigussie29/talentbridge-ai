import unittest

from career_engine import (
    analyze_job_description,
    analyze_resume_text,
    calculate_proof_based_readiness_score,
    calculate_semantic_match_score,
    compare_resume_to_job,
    generate_interview_readiness_report,
    generate_progress_tracker,
)


class TalentBridgeEngineTests(unittest.TestCase):
    def test_resume_and_job_matching(self):
        resume_skills = analyze_resume_text("Built dashboards using Python, SQL, and Power BI.")
        job_skills = analyze_job_description(
            "Seeking a data analyst with Python, SQL, Power BI, Excel, and Git."
        )

        result = compare_resume_to_job(resume_skills, job_skills)

        self.assertEqual(result["matched_skills"], ["Python", "SQL", "Power BI"])
        self.assertEqual(result["missing_skills"], ["Excel", "Git"])
        self.assertEqual(result["match_score"], 60.0)

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
