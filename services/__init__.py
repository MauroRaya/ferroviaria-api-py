from flask import Flask, Blueprint
from .db import db
from config import Config

from controllers.estacao_controller import station_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(station_bp)

    return app