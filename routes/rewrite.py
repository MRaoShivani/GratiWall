from flask import Blueprint, request, jsonify
from services.ai_service import rewrite_message

rewrite_bp = Blueprint("rewrite", __name__)


@rewrite_bp.route("/rewrite", methods=["POST"])
def rewrite_api():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({
            "status": "error",
            "message": "Field 'message' is required"
        }), 400

    user_input = data["message"].strip()
    if not user_input:
        return jsonify({
            "status": "error",
            "message": "Message cannot be empty"
        }), 400

    try:
        rewritten = rewrite_message(user_input)
        return jsonify({
            "status": "success",
            "rewritten_message": rewritten
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Rewrite failed",
            "details": str(e)
        }), 500
