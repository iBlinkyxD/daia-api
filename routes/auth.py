from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import random
import httpx

from sqlalchemy.orm import Session

from database import get_db

from models.user import User

from schemas.user import RegisterUser, RequestEmailChange

from utils.auth import get_current_user
from utils.security import hash_password, verify_password
from utils.jwt import create_access_token
from utils.verification import generate_verification_code
from utils.email import send_verification_email
from routes.users import generate_unique_username
from config import ACADEMY_API_URL, COOKIE_SECURE, COOKIE_DOMAIN, INTERNAL_SECRET

router = APIRouter()


@router.post("/register")
async def register(user: RegisterUser, db: Session = Depends(get_db)):

    # Check if email exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    code = generate_verification_code()

    username = generate_unique_username(user.first_name, user.last_name, db)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        password=hashed_password,
        username=username,
        verification_code=code,
        verification_expires=datetime.utcnow() + timedelta(minutes=10),
        is_active=True,
        is_verified=False,
        is_admin=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Notify Academy API to create the user record
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{ACADEMY_API_URL}/users/register",
                json={
                    "daia_user_id": str(new_user.id),
                    "first_name": new_user.first_name,
                    "last_name": new_user.last_name,
                },
                headers={"X-Internal-Secret": INTERNAL_SECRET},
                timeout=5.0,
            )
    except httpx.RequestError:
        # Don't fail the registration if Academy API is unreachable
        # You can add logging here later
        pass

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

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="none" if COOKIE_SECURE else "lax",
        max_age=60*60*24,
        domain=COOKIE_DOMAIN,
    )

    return {
        "access_token": token,
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "first_name": db_user.first_name,
            "last_name": db_user.last_name
        }
    }

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=COOKIE_SECURE,
        samesite="none" if COOKIE_SECURE else "lax",
        domain=COOKIE_DOMAIN,
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

@router.post("/request-email-change")
async def request_email_change(
    payload: RequestEmailChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # verify password
    if not verify_password(payload.password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Password is incorrect")

    # check if email already exists
    existing = db.query(User).filter(User.email == payload.new_email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already in use")

    # generate verification code
    code = generate_verification_code()

    # store pending email change
    current_user.pending_email = payload.new_email
    current_user.email_verification_code = code

    db.commit()

    # send verification email
    await send_verification_email(payload.new_email, code)

    return {"message": "Verification email sent"}