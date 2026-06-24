import secrets
import httpx
import jwt

from urllib.parse import urlencode

from fastapi import HTTPException, APIRouter, Depends
from fastapi.responses import RedirectResponse

from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.core.config import settings
from app.core.database import async_session
from app.models.user import User
from app.dependencies.auth import get_current_user

router = APIRouter()

pending_states: set[str] = set()

@router.get("/auth/github")
def login_with_github():
    state = secrets.token_urlsafe(16)
    pending_states.add(state)

    params = {
        "client_id": settings.github_client_id,
        "redirect_uri": "http://localhost:8000/auth/callback",
        "scope": "read:user user:email repo",
        "state": state,
    }
    github_url = f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    return RedirectResponse(github_url)

@router.get("/auth/callback")
async def github_callback(code: str, state: str):
    if state not in pending_states:
        raise HTTPException(status_code=400, detail="유효하지 않은 state입니다.")
    pending_states.discard(state)

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        access_token = token_response.json() ["access_token"]

        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        github_user = user_response.json()

    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.github_id == github_user["id"])
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                github_id=github_user["id"],
                login=github_user["login"],
                email=github_user.get("email")
            )
            session.add(user)
            await session.commit()
    
    payload = {
        "sub": str(user.id),
        "login": user.login,
        "access_token": access_token,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

    response = RedirectResponse(settings.frontend_url)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )
    return response

@router.get("/me")
def get_me(user: dict = Depends(get_current_user)):
    return {"login": user["login"]}