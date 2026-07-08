from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, webhook, reviews, repos

from app.core.config import settings

app = FastAPI(title="CodeLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(webhook.router)
app.include_router(reviews.router)
app.include_router(repos.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
