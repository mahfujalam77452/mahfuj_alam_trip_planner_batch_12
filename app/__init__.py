from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from app.extensions import db
from app.config import Config
from app.routes.trip import trip_bp
from app.routes.traveler import traveler_bp
from werkzeug.exceptions import HTTPException

def create_app():

    app = Flask(__name__)

    @app.route("/helth")
    def helth_check():
        return{
        "success":True,
        "status":"ok"
        },200
    

    app.config.from_object(Config)

    app.register_blueprint(trip_bp)
    app.register_blueprint(traveler_bp)

    db.init_app(app)

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return {
            "error":error.name,
            "message":error.description
        },error.code

    return app