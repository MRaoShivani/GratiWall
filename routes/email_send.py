from flask import Blueprint, request, jsonify
from models import db, GratitudeMessage
from services.email_service import send_gratitude_email

send_bp = Blueprint("send", __name__)


@send_bp.route("/send", methods=["POST"])
def send_email():
    data = request.get_json()

    # -------- Validation -------- #
    if not data or "gratitude_id" not in data:
        return jsonify({
            "status": "error",
            "message": "Field 'gratitude_id' is required"
        }), 400

    gratitude_id = data["gratitude_id"]

    # -------- Fetch record -------- #
    gratitude = GratitudeMessage.query.get(gratitude_id)

    if not gratitude:
        return jsonify({
            "status": "error",
            "message": "Gratitude record not found"
        }), 404

    # Prevent duplicate sends
    if gratitude.status == "EMAIL_SENT":
        return jsonify({
            "status": "error",
            "message": "Email already sent for this gratitude"
        }), 400

    try:
        # -------- Send email -------- #
        send_gratitude_email(
            to_email=gratitude.receiver_email,
            receiver_name=gratitude.receiver_name,
            sender_email=gratitude.sender_email,
            sender_name=gratitude.sender_name,
            image_path=gratitude.image_path
        )

        # -------- Update DB -------- #
        gratitude.status = "EMAIL_SENT"
        gratitude.error_message = None
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Email sent successfully"
        }), 200

    except Exception as e:
        db.session.rollback()

        # Store failure reason
        gratitude.status = "FAILED"
        gratitude.error_message = str(e)
        db.session.commit()

        return jsonify({
            "status": "error",
            "message": "Failed to send email",
            "details": str(e)
        }), 500
