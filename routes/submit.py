from flask import Blueprint, request, jsonify
from models import GratitudeMessage, db
from services.card_generator import generate_gratitude_card
import os

submit_bp = Blueprint("submit", __name__)

@submit_bp.route("/submit", methods=["POST"])
def submit_gratitude():
    data = request.get_json()  #input will be provides in raw json form from body 

    # -------- Validation -------- #
    req_fields = [
        "sender_name",
        "sender_email",  
        "receiver_name",
        "receiver_email",
        "message",
        "card_id"
    ]

    for field in req_fields:
        if field not in data or not data[field]:
            return jsonify({
                "status": "error",
                "message": f"Missing or empty field: {field}"
            }), 400

    try:
        gratitude = GratitudeMessage(
            sender_name=data["sender_name"],
            sender_email=data["sender_email"], 
            receiver_name=data["receiver_name"],
            receiver_email=data["receiver_email"],
            message=data["message"],
            card_id=data["card_id"],
            status="Received"
        )

        db.session.add(gratitude)
        db.session.commit()      #gratitude_id is generated here

        filename = f"gratitude_{gratitude.id}.png"

        image_path  = generate_gratitude_card(
            card_id=data["card_id"],
            receiver_name=data["receiver_name"],
            message=data["message"],
            sender_name=data["sender_name"],
            output_filename=filename
        )

        #storing image path in DB
        gratitude.image_path = image_path
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Gratitude message submitted successfully",
            "gratitude_id": gratitude.id,
            "image_url" : f"/{image_path}"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "details": str(e)
        }), 500
