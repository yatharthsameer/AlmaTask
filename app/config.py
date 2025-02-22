import os
from pathlib import Path

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "helloworld")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

ATTORNEY_EMAIL = os.getenv("ATTORNEY_EMAIL", "ytharthsmr@gmail.com")
