from datetime import datetime

from sqlalchemy import ForeignKey,func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    repo_full_name: Mapped[str]
    pr_number: Mapped[int]
    title: Mapped[str]
    author: Mapped[str]
    summary: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class ReviewIssue(Base):
    __tablename__ = "review_issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"))
    file: Mapped[str]
    severity: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]
    suggestion: Mapped[str]