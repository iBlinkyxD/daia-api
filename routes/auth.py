from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import random;

from sqlalchemy.orm import Session

from database import get_db

from models.user import User

from schemas.user import RegisterUser

from utils.security import hash_password, verify_password
from utils.jwt import create_access_token
from utils.verification import generate_verification_code
from utils.email import send_verification_email

router = APIRouter()

@router.post("/register")
async def register(user: RegisterUser, db: Session = Depends(get_db)):

    # Check if email exists
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    code = generate_verification_code()

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        password=hashed_password,

        verification_code = code,
        verification_expires = datetime.utcnow() + timedelta(minutes=10),

        is_active = True,
        is_verified= False,
        is_admin = False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    await send_verification_email(user.email, code)

    return {"message": "User registered successfully"}  

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    response: Response = None  # needed to set cookie
):
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="Account not active")
    if not db_user.is_verified:
        raise HTTPException(status_code=403, detail="Account not verified")

    token = create_access_token(db_user.id)

    # ✅ Set cookie without domain for localhost dev
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,        # True in production
        samesite="lax",
        max_age=60*60*24     # 1 day
    )

    return {
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "first_name": db_user.first_name,
            "last_name": db_user.last_name
        }
    }

@router.post("/logout")
def logout(response: Response):
    # ✅ Remove domain for localhost dev
    response.delete_cookie(
        key="access_token",
        path="/",
    )
    return {"message": "Logged out successfully"}

@router.post("/verify-email")
def verify_email(email: str, code: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.is_verified:
        return {"message": "Account already verified"}

    if user.verification_code != code:
        raise HTTPException(status_code=400, detail="Invalid code")

    if user.verification_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Code expired")

    user.is_verified = True
    user.verification_code = None
    user.verification_expires = None

    db.commit()

    return {"message": "Email verified successfully"}

@router.post("/resend-verification")
async def resend_verification(email: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="Account already verified")

    # generate new code
    code = str(random.randint(100000, 999999))

    user.verification_code = code
    user.verification_expires = datetime.utcnow() + timedelta(minutes=10)
    db.commit()

    await send_verification_email(user.email, code)

    return {"message": "Verification email resent"}