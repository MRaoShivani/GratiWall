from flask import Blueprint, jsonify
from models import GratitudeMessage

wall_bp = Blueprint("gratitude_wall", __name__)

@wall_bp.route("/api/gratitude-wall", methods=["GET"])
def get_gratitude_wall():
    try:
        records = (
            GratitudeMessage.query
            .filter(GratitudeMessage.image_path.isnot(None))
            .order_by(GratitudeMessage.created_at.desc())
            .all()
        )

        data = []
        for row in records:
            data.append({
                "gratitude_id": row.id,
                "image_url": "/" + row.image_path.replace("\\", "/")
            })

        return jsonify({
            "status": "success",
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to fetch gratitude wall",
            "details": str(e)
        }), 500
