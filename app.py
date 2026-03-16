import os               ###loading hugging face token
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("HF_API_TOKEN"))
import sys
print("PYTHON EXECUTABLE:", sys.executable)    ##checking the system interpreter make sure gratiwall interpreter is selected


from flask import Flask
from config import Config
from sqlalchemy import text
from models import db
from routes.submit import submit_bp
from routes.gratitude import wall_bp
from routes.rewrite import rewrite_bp
from routes.email_send import send_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(submit_bp, url_prefix="/api")
    app.register_blueprint(wall_bp)  
    app.register_blueprint(rewrite_bp,url_prefix="/api") 
    app.register_blueprint(send_bp, url_prefix="/api") 

    
    #creating the db table during first run
    # with app.app_context():
    #     db.create_all()


    @app.route("/health",methods = ['GET'])
    def health_check():
        return {"status":"ok"},200


    @app.route('/')
    def home():
        return "Flask is running"
    
    @app.route("/tables")
    def list_tables():
        result = db.session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table';")
        )
        return {"tables": [row[0] for row in result]}
    
    
    
        
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug = True)