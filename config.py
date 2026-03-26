import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")
INTERNAL_SECRET = os.getenv("INTERNAL_SECRET")

ACADEMY_API_URL = os.getenv("ACADEMY_API_URL", "http://localhost:8001").strip().rstrip("/")

# Cookies solo por HTTPS (pon COOKIE_SECURE=true detrás de Cloudflare / TLS)
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").strip().lower() in (
    "1",
    "true",
    "yes",
    "on",
)
COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", None)