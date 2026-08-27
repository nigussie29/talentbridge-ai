"""Privacy-safe recording plan for the TalentBridge AI product demo."""

from copy import deepcopy


PUBLIC_DEMO_URL = (
    "https://talentbridge-ai.streamlit.app/"
)


_DEMO_SCENES = [
    {
        "id": "opening",
        "start_seconds": 0,
        "duration_seconds": 15,
        "screen": "TalentBridge home",
        "action": "Show the signed-in Job Seeker dashboard and product overview.",
        "narration": (
            "TalentBridge AI turns a resume and job posting into an evidence-based "
            "career-readiness plan for job seekers, recruiters, and training teams."
        ),
    },
    {
        "id": "reusable_inputs",
        "start_seconds": 15,
        "duration_seconds": 25,
        "screen": "Resume & Job Match",
        "action": (
            "Open Saved Resumes and Saved Job Descriptions, then load fictional "
            "or consented demonstration inputs."
        ),
        "narration": (
            "Users can privately save and reuse their resume and job descriptions, "
            "so they do not need to copy and paste the same information repeatedly."
        ),
    },
    {
        "id": "match_results",
        "start_seconds": 40,
        "duration_seconds": 40,
        "screen": "Job Match Result",
        "action": (
            "Run the comparison and show Job Description Match, Semantic Match, "
            "Target Career Match, and Analysis Confidence."
        ),
        "narration": (
            "The analyzer separates required-skill coverage, wording and context, "
            "broader career readiness, and confidence. Each score answers a different "
            "question instead of presenting one unexplained number."
        ),
    },
    {
        "id": "evidence",
        "start_seconds": 80,
        "duration_seconds": 35,
        "screen": "Evidence details",
        "action": (
            "Open Evidence Traceability, Requirement Evidence Strength, and Critical "
            "Requirements."
        ),
        "narration": (
            "TalentBridge distinguishes strong evidence, moderate evidence, mention "
            "only, and missing evidence. It shows the resume excerpt supporting each "
            "requirement and never tells a user to invent experience."
        ),
    },
    {
        "id": "decision",
        "start_seconds": 115,
        "duration_seconds": 25,
        "screen": "Application decision",
        "action": (
            "Show the Evidence-Based Application Decision and Recommended Next Action."
        ),
        "narration": (
            "Decision guardrails combine skill coverage, evidence quality, critical "
            "gaps, and analysis reliability to recommend a truthful next action."
        ),
    },
    {
        "id": "growth",
        "start_seconds": 140,
        "duration_seconds": 25,
        "screen": "Career Readiness",
        "action": (
            "Show the learning plan, interview preparation, portfolio evidence, and "
            "saved-analysis progress dashboard."
        ),
        "narration": (
            "The result becomes a practical growth system with learning priorities, "
            "interview practice, portfolio proof, and progress tracking over time."
        ),
    },
    {
        "id": "closing",
        "start_seconds": 165,
        "duration_seconds": 15,
        "screen": "TalentBridge overview",
        "action": "Return to the overview and end on the live application.",
        "narration": (
            "TalentBridge AI connects job matching, proof, learning, and progress in "
            "one explainable workflow. Results are guidance, not an employer decision "
            "or guarantee."
        ),
    },
]


def _clock(seconds):
    """Format a number of seconds as M:SS."""
    minutes, remaining = divmod(int(seconds), 60)
    return f"{minutes}:{remaining:02d}"


def build_demo_plan(live_url=PUBLIC_DEMO_URL):
    """Return the canonical three-minute recording plan."""
    scenes = deepcopy(_DEMO_SCENES)
    for position, scene in enumerate(scenes, start=1):
        scene["number"] = position
        scene["time_range"] = (
            f"{_clock(scene['start_seconds'])}–"
            f"{_clock(scene['start_seconds'] + scene['duration_seconds'])}"
        )

    total_seconds = sum(scene["duration_seconds"] for scene in scenes)
    return {
        "title": "TalentBridge AI - 3-Minute Product Demo",
        "live_url": str(live_url or PUBLIC_DEMO_URL),
        "scenes": scenes,
        "scene_count": len(scenes),
        "total_seconds": total_seconds,
        "duration_label": _clock(total_seconds),
        "privacy_note": (
            "Record only fictional, public, or consented inputs. Hide names, email "
            "addresses, browser notifications, secrets, and private account details."
        ),
        "disclaimer": (
            "TalentBridge results are evidence-based guidance, not an employer "
            "decision. They do not verify proficiency or guarantee an interview."
        ),
    }


def build_demo_recording_checklist():
    """Return the checks required before a public demo recording."""
    return [
        {
            "id": "demo_data",
            "title": "Safe demonstration data",
            "instruction": (
                "Use fictional, public, or consented resume and job-posting text."
            ),
        },
        {
            "id": "private_details",
            "title": "Private details hidden",
            "instruction": (
                "Hide names, email addresses, saved private records, and browser "
                "account details."
            ),
        },
        {
            "id": "notifications",
            "title": "Notifications closed",
            "instruction": "Close email, chat, calendar, and desktop notifications.",
        },
        {
            "id": "display",
            "title": "Readable display",
            "instruction": (
                "Use 100% browser zoom and verify that important cards and labels "
                "are readable in the recording frame."
            ),
        },
        {
            "id": "health",
            "title": "Production health confirmed",
            "instruction": (
                "Run the Production Health Check and confirm the deployment is "
                "Operational before recording."
            ),
        },
    ]


def generate_demo_script_text(plan=None):
    """Create a portable recording and narration script."""
    demo_plan = plan or build_demo_plan()
    lines = [
        demo_plan["title"],
        "=" * len(demo_plan["title"]),
        "",
        f"Live Demo: {demo_plan['live_url']}",
        f"Target Duration: {demo_plan['duration_label']}",
        "",
        "Recording Script",
        "----------------",
    ]
    for scene in demo_plan["scenes"]:
        lines.extend(
            [
                "",
                f"Scene {scene['number']} — {scene['time_range']} — {scene['screen']}",
                f"On screen: {scene['action']}",
                f"Narration: {scene['narration']}",
            ]
        )

    lines.extend(
        [
            "",
            "Privacy",
            "-------",
            demo_plan["privacy_note"],
            "",
            "Important",
            "---------",
            demo_plan["disclaimer"],
            "",
        ]
    )
    return "\n".join(lines)
