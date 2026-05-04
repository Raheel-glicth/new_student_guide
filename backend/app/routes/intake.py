from flask import Blueprint, current_app, jsonify, request

from ..services.intake_service import save_student_intake, validate_student_intake

intake_bp = Blueprint("intake", __name__)


@intake_bp.post("/intake")
def intake():
    payload = request.get_json(silent=True) or {}
    validation_error = validate_student_intake(payload)

    if validation_error:
        return jsonify({"error": validation_error}), 400

    result = save_student_intake(current_app, payload)
    return jsonify(result), 201
