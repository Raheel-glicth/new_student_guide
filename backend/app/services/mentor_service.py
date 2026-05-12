import sqlite3

from .career_service import TRACKS
from .profile_service import fetch_student_profile
from .roadmap_service import load_dashboard_state


def _classify_intent(user_message):
    lowered = user_message.lower()
    if any(keyword in lowered for keyword in ["stuck", "overwhelmed", "confused", "lost"]):
        return "clarity"
    if any(keyword in lowered for keyword in ["motivation", "discipline", "lazy", "procrast"]):
        return "motivation"
    if any(keyword in lowered for keyword in ["project", "portfolio", "build"]):
        return "portfolio"
    if any(keyword in lowered for keyword in ["time", "busy", "schedule", "hours"]):
        return "time"
    if any(keyword in lowered for keyword in ["job", "internship", "interview", "career"]):
        return "career"
    return "next_step"


def _next_incomplete_task(roadmap):
    if roadmap is None:
        return None

    for week in roadmap["weeks"]:
        for task in week["tasks"]:
            if task["status"] != "done":
                return {
                    "week": week["week"],
                    "theme": week["theme"],
                    "task": task,
                }
    return None


def _build_action_items(intent, next_task, track_name):
    base_items = []
    if next_task:
        base_items.append(f"Complete: {next_task['task']['title']}")
        base_items.append(f"Protect one session for Week {next_task['week']} this week")
    else:
        base_items.append("Review your completed roadmap and choose the next 30-day goal")
        base_items.append("Package one finished result into a portfolio-ready proof point")

    if intent == "clarity":
        base_items.append(f"Write in one sentence why {track_name} is still worth pursuing")
    elif intent == "motivation":
        base_items.append("Lower the task size until it feels impossible to avoid")
    elif intent == "portfolio":
        base_items.append("Ship visible work before trying to perfect it")
    elif intent == "time":
        base_items.append("Reduce your weekly target to the smallest sustainable version")
    elif intent == "career":
        base_items.append("Translate your work into outcomes and evidence, not just learning")
    else:
        base_items.append("Focus on the next concrete deliverable, not the whole journey")

    return base_items


def _build_reply(profile, dashboard, user_message):
    intent = _classify_intent(user_message)
    roadmap = dashboard["roadmap"]
    progress = dashboard["progressSummary"]
    next_task = _next_incomplete_task(roadmap)
    track_name = (
        profile["targetTrackName"]
        if profile and profile["targetTrackName"]
        else "your chosen path"
    )
    track_summary = ""
    if profile and profile["targetTrackKey"] in TRACKS:
        track_summary = TRACKS[profile["targetTrackKey"]]["summary"]

    if next_task:
        next_move = (
            f"Your best next move is Week {next_task['week']}: "
            f"{next_task['task']['title']}."
        )
    else:
        next_move = "You have completed the current roadmap, so the next move is to extend it with a stronger public project."

    intent_guidance = {
        "clarity": "When you feel stuck, reduce scope and return to one measurable action for today.",
        "motivation": "Motivation usually comes after motion, so make the task smaller and start before you feel ready.",
        "portfolio": "Visible work matters more than more tutorials right now, so build, publish, and then improve.",
        "time": "A smaller weekly commitment done consistently beats an ambitious plan that collapses after two days.",
        "career": "Keep collecting proof of work because clarity and credibility both come from finished artifacts.",
        "next_step": "Momentum comes from staying close to the next deliverable instead of thinking about the whole career at once.",
    }

    reply = (
        f"You are currently aligned to {track_name}. {track_summary} "
        f"{next_move} {intent_guidance[intent]} "
        f"You have completed {progress['completedTasks']} of {progress['totalTasks']} tasks so far."
    )

    return {
        "reply": reply.strip(),
        "focusArea": intent.replace("_", " ").title(),
        "actionItems": _build_action_items(intent, next_task, track_name),
    }


def fetch_recent_messages(app, limit=8):
    with sqlite3.connect(app.config["DATABASE_PATH"]) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT role, message, created_at
            FROM mentor_messages
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {"role": row["role"], "message": row["message"], "createdAt": row["created_at"]}
        for row in reversed(rows)
    ]


def generate_placeholder_reply(app, payload):
    user_message = payload.get("message", "").strip()
    if len(user_message) > 1200:
        return {
            "reply": "That is a lot to process at once. Send the most important part in a shorter message and I will turn it into a next step.",
            "source": "local-mentor-engine",
            "actionItems": ["Shorten the question to one decision or blocker"],
            "focusArea": "Input",
            "conversation": fetch_recent_messages(app),
        }

    profile = fetch_student_profile(app)
    dashboard = load_dashboard_state(app)

    if not user_message:
        return {
            "reply": "Share what you are struggling with, and I will turn it into a concrete next move using your roadmap and progress.",
            "source": "local-mentor-engine",
            "actionItems": [],
            "focusArea": "Welcome",
            "conversation": fetch_recent_messages(app),
        }

    mentor_response = _build_reply(profile, dashboard, user_message)

    with sqlite3.connect(app.config["DATABASE_PATH"]) as connection:
        connection.execute(
            """
            INSERT INTO mentor_messages (role, message)
            VALUES (?, ?)
            """,
            ("user", user_message),
        )
        connection.execute(
            """
            INSERT INTO mentor_messages (role, message)
            VALUES (?, ?)
            """,
            ("assistant", mentor_response["reply"]),
        )
        connection.commit()

    return {
        **mentor_response,
        "source": "local-mentor-engine",
        "conversation": fetch_recent_messages(app),
    }
