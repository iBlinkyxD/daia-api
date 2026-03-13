from pydantic import BaseModel, EmailStr
from typing import Optional

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
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    profile_picture_url: Optional[str]

    class Config:
        from_attributes = True