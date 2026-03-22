import uuid
import os
from dotenv import load_dotenv

from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_access_token(user_id: uuid.UUID) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    
    payload = {
        "sub": str(user_id),  # UUID must be a string in JWT
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)