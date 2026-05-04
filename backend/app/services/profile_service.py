import json
import sqlite3


def fetch_student_profile(app):
    with sqlite3.connect(app.config["DATABASE_PATH"]) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            """
            SELECT
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
                track_scores_json,
                created_at,
                updated_at
            FROM student_profile
            WHERE id = 1
            """
        ).fetchone()

    if row is None:
        return None

    return {
        "id": row["id"],
        "fullName": row["full_name"],
        "educationLevel": row["education_level"],
        "interestAreas": json.loads(row["interest_areas_json"] or "[]"),
        "goals": row["goals"] or "",
        "answers": json.loads(row["answers_json"] or "{}"),
        "targetTrackKey": row["target_track_key"] or "",
        "targetTrackName": row["target_track_name"] or "",
        "weeklyCommitment": row["weekly_commitment"] or "",
        "learningStyle": row["learning_style"] or "",
        "scoreBreakdown": json.loads(row["track_scores_json"] or "[]"),
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
    }

