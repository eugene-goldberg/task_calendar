import os
from dotenv import load_dotenv

# Load environment variables from .env file in development
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL", "")

# Handle different PostgreSQL URL formats
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    # Check if it's already using a specific dialect
    if "+psycopg" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# If no DATABASE_URL in environment, use local development database
if not DATABASE_URL:
    DATABASE_URL = "postgresql+psycopg://calendar_user:calendar_pass@localhost:5433/calendar_db"

# Other configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"

# CORS origins
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
if ALLOWED_ORIGINS == ["*"] and ENVIRONMENT == "production":
    # In production, specify actual origins
    ALLOWED_ORIGINS = [
        "https://your-app-name.herokuapp.com",
        "https://your-custom-domain.com"
    ]