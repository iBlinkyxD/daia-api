import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routes import auth, users

app = FastAPI()

_default_origins = [
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8082",
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

app.include_router(auth.router)
app.include_router(users.router)