from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db, jwt, migrate
from app.routes.workflow_steps import workflow_steps_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for React frontend
    CORS(
    app,
    resources={r"/*": {"origins": [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://dcm-star-portfolio.vercel.app",
        "https://workflow-automation-builder-lake.vercel.app"
    ]}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app import models

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.workflows import workflows_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(workflows_bp)
    app.register_blueprint(workflow_steps_bp)

    @app.route("/health", methods=["GET"])
    def health_check():
        return {"status": "ok"}, 200

    return app