from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "codelens",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.services.pr_review"],
)