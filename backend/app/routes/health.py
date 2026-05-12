from flask import Blueprint, current_app, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check():
    return jsonify(
        {
            "status": "ok",
            "service": "ai-career-os-backend",
            "version": current_app.config["APP_VERSION"],
            "environment": current_app.config["APP_ENV"],
            "database": "ready",
            "mentorProvider": current_app.config["MENTOR_PROVIDER"],
            "port": current_app.config["PORT"],
        }
    )
