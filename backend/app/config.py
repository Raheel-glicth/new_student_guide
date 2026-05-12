import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def _get_bool(name, default="false"):
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


class Config:
    APP_NAME = "student-decisoom"
    APP_VERSION = os.getenv("APP_VERSION", "0.3.0")
    APP_ENV = os.getenv(
        "APP_ENV",
        "production" if os.getenv("VERCEL") else os.getenv("FLASK_ENV", "development"),
    )
    PORT = int(os.getenv("PORT", "5000"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(128 * 1024)))
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
    ENABLE_REQUEST_LOGGING = _get_bool("ENABLE_REQUEST_LOGGING", "true")
    ENABLE_RATE_LIMITING = _get_bool("ENABLE_RATE_LIMITING", "true")
    MENTOR_PROVIDER = os.getenv("MENTOR_PROVIDER", "local")
    RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
    RATE_LIMITS = {
        "/api/intake": int(os.getenv("INTAKE_RATE_LIMIT", "12")),
        "/api/mentor": int(os.getenv("MENTOR_RATE_LIMIT", "20")),
    }
