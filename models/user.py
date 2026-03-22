import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )


    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    
    password = Column(String, nullable=False)

    profile_picture_url = Column(String, nullable=True)
    
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    verification_code = Column(String, nullable=True)
    verification_expires = Column(DateTime, nullable=True)

    pending_email = Column(String, nullable=True)
    email_verification_code = Column(String, nullable=True)
    email_verification_expires = Column(DateTime, nullable=True)