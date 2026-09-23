import os
from flask import Flask, jsonify
from marshmallow import ValidationError
from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors, limiter

def create_app():
    app = Flask(__name__)
    env = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config_by_name[env])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config.get("CORS_ORIGINS", []))
    limiter.init_app(app)

    from app import models  # noqa: F401
    from app.resources.users import users_bp
    from app.resources.auth import auth_bp

    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"message": "Internal server error"}), 500

    @app.errorhandler(429)
    def rate_limit_error(e):
        return jsonify({"message": "Too many requests, please try again later"}), 429

    @app.errorhandler(ValidationError)
    def validation_error(e):
        return jsonify({"message": "Validation error", "errors": e.messages}), 400

    return app
