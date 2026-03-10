from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from models.user import User

from utils.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_current_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return {"user": current_user}