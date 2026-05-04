import sqlite3


VALID_STATUSES = {"pending", "in_progress", "done"}


def save_progress_update(app, payload):
    roadmap_id = payload.get("roadmapId")
    week_number = payload.get("weekNumber")
    task_key = payload.get("taskKey", "").strip()
    task_title = payload.get("taskTitle", "").strip()
    status = payload.get("status", "pending")
    notes = payload.get("notes", "")

    if roadmap_id is None or week_number is None or not task_title or not task_key:
        return {
            "message": "roadmapId, weekNumber, taskKey, and taskTitle are required.",
            "saved": False,
        }

    if status not in VALID_STATUSES:
        return {
            "message": "status must be pending, in_progress, or done.",
            "saved": False,
        }

    with sqlite3.connect(app.config["DATABASE_PATH"]) as connection:
        cursor = connection.execute(
            """
            INSERT INTO progress_entries (
                roadmap_id,
                week_number,
                task_key,
                task_title,
                status,
                notes,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(roadmap_id, task_key) DO UPDATE SET
                week_number = excluded.week_number,
                task_title = excluded.task_title,
                status = excluded.status,
                notes = excluded.notes,
                updated_at = CURRENT_TIMESTAMP
            """,
            (roadmap_id, week_number, task_key, task_title, status, notes),
        )
        connection.commit()

    return {
        "message": "Progress saved successfully.",
        "saved": True,
        "progressId": cursor.lastrowid,
    }


def fetch_progress_map(app, roadmap_id):
    with sqlite3.connect(app.config["DATABASE_PATH"]) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT task_key, task_title, status, notes, week_number, updated_at
            FROM progress_entries
            WHERE roadmap_id = ?
            """,
            (roadmap_id,),
        ).fetchall()

    return {
        row["task_key"]: {
            "taskTitle": row["task_title"],
            "status": row["status"],
            "notes": row["notes"] or "",
            "weekNumber": row["week_number"],
            "updatedAt": row["updated_at"],
        }
        for row in rows
        if row["task_key"]
    }


def build_progress_summary(roadmap):
    tasks = []
    for week in roadmap["weeks"]:
        tasks.extend(week["tasks"])

    total_tasks = len(tasks)
    completed = sum(1 for task in tasks if task["status"] == "done")
    in_progress = sum(1 for task in tasks if task["status"] == "in_progress")
    pending = total_tasks - completed - in_progress
    completion_rate = int((completed / total_tasks) * 100) if total_tasks else 0

    return {
        "totalTasks": total_tasks,
        "completedTasks": completed,
        "inProgressTasks": in_progress,
        "pendingTasks": pending,
        "completionRate": completion_rate,
    }
