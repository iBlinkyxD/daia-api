import re
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.user import UpdateProfileRequest, UserResponse, ChangePasswordRequest, PublicProfileResponse
from utils.auth import get_current_user
from utils.security import verify_password, hash_password
from services.storage import upload_avatar

router = APIRouter(prefix="/users", tags=["users"])


def generate_unique_username(first_name: str, last_name: str, db: Session) -> str:
    base = re.sub(r"[^a-z0-9]", "", f"{first_name}{last_name}".lower())
    username = base
    counter = 2
    while db.query(User).filter(User.username == username).first():
        username = f"{base}{counter}"
        counter += 1
    return username


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/profile/{username}", response_model=PublicProfileResponse)
def get_public_profile(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Profile not found")
    return user


@router.put("/me", response_model=UserResponse)
def update_profile(
    payload: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.first_name:
        current_user.first_name = payload.first_name

    if payload.last_name:
        current_user.last_name = payload.last_name

    if payload.phone:
        current_user.phone = payload.phone

    db.commit()
    db.refresh(current_user)

    return current_user


@router.post("/me/avatar")
async def upload_my_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if file.content_type not in ["image/png", "image/jpeg", "image/webp"]:
        raise HTTPException(status_code=400, detail="Invalid image type")

    contents = await file.read()
    filename = f"{current_user.id}/{uuid.uuid4()}.{file.filename.split('.')[-1]}"

    url = upload_avatar(contents, filename, file.content_type)

    current_user.profile_picture_url = url
    db.commit()

    return {"avatar_url": url}


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(payload.current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    current_user.password = hash_password(payload.new_password)

    db.commit()
    db.refresh(current_user)

    return {"message": "Password updated successfully"}