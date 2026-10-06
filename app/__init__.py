from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from app.extensions import db
from app.config import Config
from app.routes.trip import trip_bp

def create_app():

    app = Flask(__name__)

    @app.route("/helth")
    def helth_check():
        return{
        "success":True,
        "message":"server helth is ok"
        },200
    

    app.config.from_object(Config)

    app.register_blueprint(trip_bp)

    db.init_app(app)

    return app