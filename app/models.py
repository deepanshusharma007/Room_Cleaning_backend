from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database import Base


class Admin(Base):

    __tablename__ = "admins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = Column(String, unique=True, nullable=False)

    password_hash = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class CleaningReceipt(Base):

    __tablename__ = "cleaning_receipts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    cleaner_name = Column(String, nullable=False)

    room_number = Column(String, nullable=False)

    image_url = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    admin_id = Column(
        UUID(as_uuid=True),
        ForeignKey("admins.id")
    )

    token = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)