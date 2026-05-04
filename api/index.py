import os
import sys
from pathlib import Path
from flask import send_from_directory


ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIST_DIR = ROOT_DIR / "frontend" / "dist"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Ensure Flask sees project paths correctly on Vercel.
os.environ.setdefault("DATABASE_PATH", "/tmp/student_os.db")

from app import create_app  # noqa: E402

app = create_app()


@app.get("/")
def serve_frontend_root():
    return send_from_directory(FRONTEND_DIST_DIR, "index.html")


@app.get("/<path:path>")
def serve_frontend_assets(path):
    requested_path = FRONTEND_DIST_DIR / path
    if requested_path.exists() and requested_path.is_file():
        return send_from_directory(FRONTEND_DIST_DIR, path)
    return send_from_directory(FRONTEND_DIST_DIR, "index.html")
