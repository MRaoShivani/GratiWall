from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GratitudeMessage(db.Model):
    __tablename__ ="gratitude_message"

    id = db.Column( db.Integer, primary_key = True)
    sender_name = db.Column(db.String, nullable = False)
    sender_email = db.Column(db.String, nullable=True)
    receiver_name = db.Column(db.String, nullable = False)
    receiver_email = db.Column(db.String, nullable = False)
    message = db.Column(db.Text)
    card_id = db.Column(db.Integer,nullable = False)
    status = db.Column(db.String)
    error_message = db.Column(db.Text)
    image_path = db.Column(db.String)
    created_at = db.Column(db.DateTime,server_default = db.func.current_timestamp())

    def __repr__(self):
        return f"<GratitudeMessage id ={self.id}>"

    
