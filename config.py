import os

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "my_super_secret_key_2026"
    UPLOAD_FOLDER = "uploads"

    ADMIN_USERNAME = "rachit"
    ADMIN_PASSWORD = "rptl"

    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024   # 500 MB

    # Allowed video extensions
    ALLOWED_EXTENSIONS = {
        "mp4",
        "mov",
        "mkv",
        "avi",
        "webm"
    }

    # SQLite database
    DATABASE = os.path.join(BASE_DIR, "database.db")

    # Admin login (for practice)
    ADMIN_USERNAME = "rachit"
    ADMIN_PASSWORD = "rptl"

    # Contact details
    PHONE_NUMBER = "++919316763783"
    WHATSAPP_NUMBER = "919316763783"

    # Categories
    CATEGORIES = [
        "Gaming",
        "Status",
        "Education",
        "Technology",
        "Entertainment",
        "Vlog",
        "Music",
        "Other"
    ]
