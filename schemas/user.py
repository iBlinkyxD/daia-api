from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class RegisterUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UpdateProfileRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    username: Optional[str]
    profile_picture_url: Optional[str]

    class Config:
        from_attributes = True


class PublicProfileResponse(BaseModel):
    first_name: str
    last_name: str
    username: str
    profile_picture_url: Optional[str]

    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class RequestEmailChange(BaseModel):
    new_email: str
    password: str