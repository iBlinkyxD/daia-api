import os
from dotenv import load_dotenv

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")
INTERNAL_SECRET = os.getenv("INTERNAL_SECRET")

_env = os.getenv("ENVIRONMENT", "development").strip().lower()
_academy_override = os.getenv("ACADEMY_API_URL", "").strip().rstrip("/")
if _academy_override:
    ACADEMY_API_URL = _academy_override
elif _env in ("production", "prod"):
    ACADEMY_API_URL = "web-production-ea951.up.railway.app"
else:
    ACADEMY_API_URL = "http://localhost:8001"

# Cookies solo por HTTPS (pon COOKIE_SECURE=true detrás de Cloudflare / TLS)
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").strip().lower() in (
    "1",
    "true",
    "yes",
    "on",
)