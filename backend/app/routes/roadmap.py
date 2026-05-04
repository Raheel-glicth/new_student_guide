from flask import Blueprint, current_app, jsonify

from ..services.roadmap_service import load_dashboard_state

roadmap_bp = Blueprint("roadmap", __name__)


@roadmap_bp.get("/roadmap")
def get_roadmap():
    dashboard = load_dashboard_state(current_app)

    if dashboard["roadmap"] is None:
        return jsonify(
            {
                "roadmap": None,
                "message": "No roadmap generated yet. Submit intake first.",
                "profile": dashboard["profile"],
                "recommendation": dashboard["recommendation"],
                "progressSummary": dashboard["progressSummary"],
            }
        )

    return jsonify(dashboard)
