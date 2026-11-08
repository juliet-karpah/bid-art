
from app.db.base import Base
from datetime import datetime
from sqlalchemy import DateTime, func, Uuid
from sqlalchemy.orm import Mapped, mapped_column
import uuid


class User(Base):
    __tablename__ = "users"

    id:Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    email:Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    role: Mapped[str] = mapped_column(default="seller")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())




