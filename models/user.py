import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class User(Base):
    # Tabla distinta de Academy `users` (shadow con daia_user_id). Evita mezclar esquemas en la misma tabla.
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

    username = Column(String, unique=True, index=True, nullable=True)

    profile_picture_url = Column(String, nullable=True)

    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    verification_code = Column(String, nullable=True)
    verification_expires = Column(DateTime, nullable=True)

    pending_email = Column(String, nullable=True)
    email_verification_code = Column(String, nullable=True)
    email_verification_expires = Column(DateTime, nullable=True)

    reset_password_token = Column(String, nullable=True, index=True)
    reset_password_expires = Column(DateTime, nullable=True)