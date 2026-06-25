from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.core.database import async_session
from app.dependencies.auth import get_current_user
from app.models import Review, ReviewIssue

router = APIRouter()


@router.get("/reviews")
async def list_reviews(user: dict = Depends(get_current_user)):
    async with async_session() as session:
        result = await session.execute(select(Review).order_by(Review.created_at.desc()))
        reviews = result.scalars().all()
        return [
            {
                "id": r.id,
                "repo_full_name": r.repo_full_name,
                "pr_number": r.pr_number,
                "summary": r.summary,
                "created_at": r.created_at,
            }
            for r in reviews
        ]


@router.get("/reviews/{review_id}")
async def get_review(review_id: int, user: dict = Depends(get_current_user)):
    async with async_session() as session:
        review = await session.get(Review, review_id)
        if review is None:
            raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다")

        result = await session.execute(select(ReviewIssue).where(ReviewIssue.review_id == review_id))
        issues = result.scalars().all()

        return {
            "id": review.id,
            "repo_full_name": review.repo_full_name,
            "pr_number": review.pr_number,
            "summary": review.summary,
            "created_at": review.created_at,
            "issues": [
                {
                    "id": i.id,
                    "file": i.file,
                    "severity": i.severity,
                    "title": i.title,
                    "description": i.description,
                    "suggestion": i.suggestion,
                }
                for i in issues
            ],
        }