from flask import Blueprint, current_app, jsonify, request

from ..services.mentor_service import generate_placeholder_reply

mentor_bp = Blueprint("mentor", __name__)


@mentor_bp.post("/mentor")
def mentor():
    payload = request.get_json(silent=True) or {}

    reply = generate_placeholder_reply(current_app, payload)
    return jsonify(reply)

