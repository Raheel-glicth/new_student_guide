from pathlib import Path
import sqlite3


SCHEMA = """
CREATE TABLE IF NOT EXISTS student_profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    full_name TEXT NOT NULL,
    education_level TEXT,
    interest_areas_json TEXT NOT NULL DEFAULT '[]',
    goals TEXT,
    answers_json TEXT NOT NULL DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS roadmaps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    weeks_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS progress_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roadmap_id INTEGER NOT NULL,
    week_number INTEGER NOT NULL,
    task_title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    notes TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mentor_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def ensure_column(connection, table_name, column_name, column_definition):
    columns = {
        row[1]
        for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    }
    if column_name not in columns:
        connection.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
        )


def init_db(app):
    database_path = Path(app.config["DATABASE_PATH"])
    database_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database_path) as connection:
        connection.executescript(SCHEMA)
        ensure_column(connection, "student_profile", "target_track_key", "TEXT")
        ensure_column(connection, "student_profile", "target_track_name", "TEXT")
        ensure_column(connection, "student_profile", "weekly_commitment", "TEXT")
        ensure_column(connection, "student_profile", "learning_style", "TEXT")
        ensure_column(connection, "student_profile", "track_scores_json", "TEXT DEFAULT '[]'")
        ensure_column(connection, "progress_entries", "task_key", "TEXT")
        ensure_column(
            connection,
            "progress_entries",
            "updated_at",
            "TEXT",
        )
        connection.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_progress_entries_task
            ON progress_entries (roadmap_id, task_key)
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_roadmaps_profile_created
            ON roadmaps (profile_id, created_at DESC)
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_mentor_messages_created
            ON mentor_messages (created_at DESC)
            """
        )
        connection.commit()
