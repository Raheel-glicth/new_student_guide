import json
import sqlite3

from .career_service import TRACKS
from .profile_service import fetch_student_profile
from .progress_service import build_progress_summary, fetch_progress_map


def _task(task_key, title, description):
    return {
        "key": task_key,
        "title": title,
        "description": description,
        "status": "pending",
        "notes": "",
    }


def generate_personalized_roadmap(payload, recommendation):
    primary_track = recommendation["primaryTrack"]
    track_data = TRACKS[primary_track["key"]]
    student_goal = payload.get("goals", "Build a strong foundation and create visible proof of work.")
    weekly_commitment = recommendation["weeklyCommitment"]
    pace_label = recommendation["paceLabel"]
    tool_one = track_data["tools"][0]
    tool_two = track_data["tools"][1]

    weeks = [
        {
            "week": 1,
            "theme": "Self-discovery and setup",
            "outcome": "Turn your ambition into a focused learning plan and setup.",
            "tasks": [
                _task(
                    "w1-clarity",
                    f"Write your {primary_track['name']} target statement",
                    f"Describe why this path matters to you and connect it to your goal: {student_goal}",
                ),
                _task(
                    "w1-schedule",
                    "Lock your weekly study rhythm",
                    f"Create a {weekly_commitment} study schedule and protect at least three focused sessions.",
                ),
                _task(
                    "w1-tools",
                    f"Install your starter stack: {tool_one} and {tool_two}",
                    "Set up the main tools and verify you can complete one basic practice task.",
                ),
            ],
        },
        {
            "week": 2,
            "theme": "Core foundations",
            "outcome": "Build confidence with the baseline concepts and vocabulary.",
            "tasks": [
                _task(
                    "w2-concepts",
                    f"Study the fundamentals of {primary_track['name']}",
                    f"Focus on these skills: {', '.join(track_data['focus_skills'][:3])}.",
                ),
                _task(
                    "w2-notes",
                    "Create a public or personal learning log",
                    "Summarize what you learn each session in one note, screenshot, or progress post.",
                ),
                _task(
                    "w2-mini",
                    "Finish one mini exercise",
                    f"Choose a small exercise that can be completed in a {pace_label} weekly pace.",
                ),
            ],
        },
        {
            "week": 3,
            "theme": "Guided practice",
            "outcome": "Move from passive learning into repeatable practice.",
            "tasks": [
                _task(
                    "w3-research",
                    "Analyze real career examples",
                    f"Review 3 examples of real {primary_track['name']} work and note common patterns.",
                ),
                _task(
                    "w3-skill",
                    "Deepen one high-value skill",
                    f"Spend focused time on the skill that feels most important right now: {track_data['focus_skills'][0]}.",
                ),
                _task(
                    "w3-feedback",
                    "Ask for feedback or self-review",
                    "Review your output critically and record what should improve next week.",
                ),
            ],
        },
        {
            "week": 4,
            "theme": "Portfolio project planning",
            "outcome": "Define a project that proves direction, consistency, and ability.",
            "tasks": [
                _task(
                    "w4-project-scope",
                    "Scope your starter project",
                    track_data["project"],
                ),
                _task(
                    "w4-breakdown",
                    "Break the project into milestones",
                    "Create milestones for planning, building, polishing, and publishing.",
                ),
                _task(
                    "w4-start",
                    "Start the first build session",
                    "Complete the first meaningful deliverable and capture proof of progress.",
                ),
            ],
        },
        {
            "week": 5,
            "theme": "Project execution",
            "outcome": "Complete the strongest version of your first proof-of-work piece.",
            "tasks": [
                _task(
                    "w5-build",
                    "Finish the core project deliverable",
                    "Push the project to a visible draft you can show another person.",
                ),
                _task(
                    "w5-refine",
                    "Polish the output",
                    "Improve clarity, quality, or usability based on feedback and self-review.",
                ),
                _task(
                    "w5-story",
                    "Write the story behind your work",
                    "Document the problem, approach, tools, and what you learned.",
                ),
            ],
        },
        {
            "week": 6,
            "theme": "Career launch system",
            "outcome": "Turn momentum into a repeatable next-step system.",
            "tasks": [
                _task(
                    "w6-publish",
                    "Publish your work",
                    "Share the project in a portfolio, drive folder, Behance page, GitHub repo, or social post.",
                ),
                _task(
                    "w6-gap",
                    "Identify your next skill gap",
                    "Choose the single most valuable next skill to strengthen after this roadmap.",
                ),
                _task(
                    "w6-system",
                    "Set your next 30-day operating system",
                    "Define weekly learning hours, portfolio targets, and one accountability mechanism.",
                ),
            ],
        },
    ]

    return {
        "title": f"{primary_track['name']} Career Roadmap",
        "summary": f"A six-week roadmap tailored for a student targeting {primary_track['name']}.",
        "weeks": weeks,
    }


def _merge_progress(roadmap, progress_map):
    if roadmap is None:
        return None

    merged_weeks = []
    for week in roadmap["weeks"]:
        week_tasks = []
        for task in week["tasks"]:
            saved_progress = progress_map.get(task["key"], {})
            week_tasks.append(
                {
                    **task,
                    "status": saved_progress.get("status", task.get("status", "pending")),
                    "notes": saved_progress.get("notes", task.get("notes", "")),
                }
            )

        merged_weeks.append({**week, "tasks": week_tasks})

    return {**roadmap, "weeks": merged_weeks}


def fetch_latest_roadmap(app):
    with sqlite3.connect(app.config["DATABASE_PATH"]) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            """
            SELECT id, title, summary, weeks_json, created_at
            FROM roadmaps
            ORDER BY id DESC
            LIMIT 1
            """
        ).fetchone()

    if row is None:
        return None

    return {
        "id": row["id"],
        "title": row["title"],
        "summary": row["summary"],
        "weeks": json.loads(row["weeks_json"]),
        "createdAt": row["created_at"],
    }


def load_dashboard_state(app):
    profile = fetch_student_profile(app)
    roadmap = fetch_latest_roadmap(app)

    if roadmap is None:
        return {
            "profile": profile,
            "recommendation": None,
            "roadmap": None,
            "progressSummary": {
                "totalTasks": 0,
                "completedTasks": 0,
                "inProgressTasks": 0,
                "pendingTasks": 0,
                "completionRate": 0,
            },
        }

    progress_map = fetch_progress_map(app, roadmap["id"])
    roadmap = _merge_progress(roadmap, progress_map)
    progress_summary = build_progress_summary(roadmap)
    recommendation = None

    if profile and profile["targetTrackName"]:
        primary_track = TRACKS.get(profile["targetTrackKey"], {})
        recommendation = {
            "primaryTrack": {
                "key": profile["targetTrackKey"],
                "name": profile["targetTrackName"],
                "summary": primary_track.get("summary", ""),
                "tools": primary_track.get("tools", []),
                "projectIdea": primary_track.get("project", ""),
                "focusSkills": primary_track.get("focus_skills", []),
                "whyFit": [],
            },
            "alternatives": profile["scoreBreakdown"][1:4] if profile["scoreBreakdown"] else [],
            "scoreBreakdown": profile["scoreBreakdown"],
            "weeklyCommitment": profile["weeklyCommitment"],
            "paceLabel": "",
        }

    return {
        "profile": profile,
        "recommendation": recommendation,
        "roadmap": roadmap,
        "progressSummary": progress_summary,
    }
