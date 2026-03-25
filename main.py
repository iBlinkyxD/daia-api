import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routes import auth, users

app = FastAPI()

_default_origins = [
    "http://localhost:8080",  # landing
    "http://localhost:8081",  # hub
    "http://localhost:8082",  # academy

    "https://daia-landing.netlify.app",
    "https://daia-hub-app.netlify.app",
    "https://daia-academy-app.netlify.app",
]

_cors_env = os.getenv("CORS_ORIGINS", "").strip()
origins = (
    [o.strip() for o in _cors_env.split(",") if o.strip()]
    if _cors_env
    else _default_origins
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables in PostgreSQL
Base.metadata.create_all(bind=engine)

# Apply any column additions that create_all won't handle on existing tables
with engine.connect() as conn:
    conn.execute(
        __import__("sqlalchemy").text(
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS username VARCHAR UNIQUE"
        )
    )
    conn.commit()

app.include_router(auth.router)
app.include_router(users.router)