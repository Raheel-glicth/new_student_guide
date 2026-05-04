from flask import Flask
from flask_cors import CORS

from .config import Config
from .db import init_db
from .routes.health import health_bp
from .routes.intake import intake_bp
from .routes.roadmap import roadmap_bp
from .routes.progress import progress_bp
from .routes.mentor import mentor_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    init_db(app)

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(intake_bp, url_prefix="/api")
    app.register_blueprint(roadmap_bp, url_prefix="/api")
    app.register_blueprint(progress_bp, url_prefix="/api")
    app.register_blueprint(mentor_bp, url_prefix="/api")

    return app

