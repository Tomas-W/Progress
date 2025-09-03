import os

from enum import Enum
from flask import (
    Flask, 
)

from routes.landing.landing_route import landing_bp
from routes.home.home_routes import home_bp
from routes.admin.admin_routes import admin_bp

from utils.config import CFG


def get_app() -> Flask:
    """Initializes the Flask app."""
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

    _init_security_headers(app)
    _init_session(app)
    _init_blueprints(app)
    return app


def _init_security_headers(app: Flask) -> None:
    app.config["SECURITY_HEADERS"] = CFG.server.SECURITY_HEADERS
    @app.after_request
    def add_security_headers(response):
        for header, value in app.config["SECURITY_HEADERS"].items():
            response.headers[header] = value
        return response


def _init_session(app: Flask) -> None:
    app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))
    
    is_production = os.environ.get("DEBUG") == "False"
    
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=is_production,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=2592000,
        SESSION_COOKIE_NAME='tracker_session',
        SESSION_COOKIE_PATH='/',
        SESSION_PROTECTION='strong',
        SESSION_REFRESH_EACH_REQUEST=False
    )

def _init_blueprints(app):
    app.register_blueprint(landing_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)


class ContentType(Enum):
    """Content types with their cache settings"""
    STATIC = ["application/javascript", "image/", "font/"]
    DOCUMENT = ["text/html", "text/css"]
    API = ["application/json", "application/xml"]
