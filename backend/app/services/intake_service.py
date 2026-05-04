import json
import sqlite3

from .career_service import (
    INTEREST_TO_TRACK,
    PACE_LABELS,
    QUESTION_SCORING,
    score_student_profile,
)
from .roadmap_service import generate_personalized_roadmap, load_dashboard_state


def validate_student_intake(payload):
    full_name = payload.get("fullName", "").strip()
    education_level = payload.get("educationLevel", "").strip()
    interest_areas = payload.get("interestAreas", [])
    goals = payload.get("goals", "").strip()
    answers = payload.get("answers", {})

    if not full_name:
        return "fullName is required."
    if not education_level:
        return "educationLevel is required."
    if not isinstance(interest_areas, list) or not interest_areas:
        return "Select at least one interest area."
    if any(interest not in INTEREST_TO_TRACK for interest in interest_areas):
        return "One or more interest areas are not supported."
    if not goals:
        return "goals is required."
    if not isinstance(answers, dict):
        return "answers must be an object."

    required_questions = [
        "workStyle",
        "energySource",
        "toolPreference",
        "learningStyle",
        "collaborationStyle",
        "weeklyCommitment",
        "preferredOutcome",
    ]

    for question_key in required_questions:
        answer_value = answers.get(question_key)
        if question_key == "weeklyCommitment":
            if not answer_value or answer_value not in PACE_LABELS:
                return "Answer weeklyCommitment with a supported option."
            continue

        valid_values = QUESTION_SCORING.get(question_key, {})
        if not answer_value or answer_value not in valid_values:
            return f"Answer {question_key} with a supported option."

    return ""


def save_student_intake(app, payload):
    full_name = payload.get("fullName", "Student").strip()
    education_level = payload.get("educationLevel", "Not specified").strip()
    interest_areas = payload.get("interestAreas", [])
    goals = payload.get("goals", "").strip()
    answers = payload.get("answers", {})
    recommendation = score_student_profile(payload)
    primary_track = recommendation["primaryTrack"]

    with sqlite3.connect(app.config["DATABASE_PATH"]) as connection:
        connection.execute(
            """
            INSERT INTO student_profile (
                id,
                full_name,
                education_level,
                interest_areas_json,
                goals,
                answers_json,
                target_track_key,
                target_track_name,
                weekly_commitment,
                learning_style,
                track_scores_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                full_name = excluded.full_name,
                education_level = excluded.education_level,
                interest_areas_json = excluded.interest_areas_json,
                goals = excluded.goals,
                answers_json = excluded.answers_json,
                target_track_key = excluded.target_track_key,
                target_track_name = excluded.target_track_name,
                weekly_commitment = excluded.weekly_commitment,
                learning_style = excluded.learning_style,
                track_scores_json = excluded.track_scores_json,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                1,
                full_name,
                education_level,
                json.dumps(interest_areas),
                goals,
                json.dumps(answers),
                primary_track["key"],
                primary_track["name"],
                recommendation["weeklyCommitment"],
                answers.get("learningStyle", ""),
                json.dumps(recommendation["scoreBreakdown"]),
            ),
        )

        roadmap = generate_personalized_roadmap(payload, recommendation)
        cursor = connection.execute(
            """
            INSERT INTO roadmaps (profile_id, title, summary, weeks_json)
            VALUES (?, ?, ?, ?)
            """,
            (
                1,
                roadmap["title"],
                roadmap["summary"],
                json.dumps(roadmap["weeks"]),
            ),
        )
        roadmap_id = cursor.lastrowid
        connection.commit()

    dashboard = load_dashboard_state(app)

    return {
        "message": "Intake saved successfully.",
        "profile": {
            "fullName": full_name,
            "educationLevel": education_level,
            "interestAreas": interest_areas,
        },
        "recommendation": recommendation,
        "roadmapId": roadmap_id,
        "dashboard": dashboard,
    }
