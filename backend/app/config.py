import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    PORT = int(os.getenv("PORT", "5000"))
    DATABASE_PATH = os.getenv(
        "DATABASE_PATH",
        str(BASE_DIR / "app" / "db" / "student_os.db"),
    )
    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
