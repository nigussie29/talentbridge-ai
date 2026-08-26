import unittest

from demo_service import (
    build_demo_plan,
    build_demo_recording_checklist,
    generate_demo_script_text,
)


class DemoServiceTests(unittest.TestCase):
    def test_demo_plan_is_exactly_three_minutes(self):
        plan = build_demo_plan()

        self.assertEqual(plan["total_seconds"], 180)
        self.assertEqual(plan["duration_label"], "3:00")
        self.assertEqual(plan["scene_count"], 7)
        self.assertEqual(plan["scenes"][0]["time_range"], "0:00–0:15")
        self.assertEqual(plan["scenes"][-1]["time_range"], "2:45–3:00")

    def test_demo_plan_covers_core_product_story(self):
        plan = build_demo_plan()
        scene_ids = {scene["id"] for scene in plan["scenes"]}

        self.assertEqual(
            scene_ids,
            {
                "opening",
                "reusable_inputs",
                "match_results",
                "evidence",
                "decision",
                "growth",
                "closing",
            },
        )
        self.assertIn("not an employer decision", plan["disclaimer"])

    def test_recording_checklist_is_complete_and_unique(self):
        checklist = build_demo_recording_checklist()

        self.assertEqual(len(checklist), 5)
        self.assertEqual(len({item["id"] for item in checklist}), 5)
        self.assertTrue(all(item["title"] and item["instruction"] for item in checklist))

    def test_demo_script_contains_timing_privacy_and_disclaimer(self):
        script = generate_demo_script_text(build_demo_plan("https://example.test"))

        self.assertIn("https://example.test", script)
        self.assertIn("Scene 1 — 0:00–0:15", script)
        self.assertIn("Scene 7 — 2:45–3:00", script)
        self.assertIn("fictional, public, or consented", script)
        self.assertIn("do not verify proficiency", script)


if __name__ == "__main__":
    unittest.main()
