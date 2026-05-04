from flask import Blueprint, current_app, jsonify, request

from ..services.progress_service import save_progress_update

progress_bp = Blueprint("progress", __name__)


@progress_bp.post("/progress")
def record_progress():
    payload = request.get_json(silent=True) or {}

    result = save_progress_update(current_app, payload)
    status_code = 201 if result["saved"] else 400
    return jsonify(result), status_code
