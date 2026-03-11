from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routes import auth, users

app = FastAPI()

origins = [
    "http://localhost:8080",  # landing
    "http://localhost:8081",  # hub
    "http://localhost:8082",  # academy
]

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