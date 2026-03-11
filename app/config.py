import os
from datetime import timedelta


class Config:
    # Core Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # JWT
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # Database Environment Variables
    DB_USER = os.getenv("DB_USER", "admin")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv(
        "DB_HOST",
        "workflow-db.cmp6yo20qbnq.us-east-1.rds.amazonaws.com"
    )
    DB_NAME = os.getenv("DB_NAME", "workflow_db")

    # SQLAlchemy Database URI
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False