from flask import Blueprint, current_app, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check():
    return jsonify(
        {
            "status": "ok",
            "service": "ai-career-os-backend",
            "database": "ready",
            "port": current_app.config["PORT"],
        }
    )

