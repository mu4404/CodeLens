from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    github_id: Mapped[int] = mapped_column(unique=True, index=True)
    login: Mapped[str]
    email: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())