from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete

import httpx

from app.core.config import settings
from app.core.database import async_session
from app.dependencies.auth import get_current_user
from app.models.repository import Repository

router = APIRouter()


@router.get("/repos")
async def list_repos(user: dict = Depends(get_current_user)):
    access_token = user["access_token"]

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"per_page": 100, "sort": "updated"},
        )
        github_repos = response.json()

    async with async_session() as session:
        result = await session.execute(
            select(Repository).where(Repository.user_id == int(user["sub"]))
        )
        connected = {r.repo_full_name for r in result.scalars().all()}

    return [
        {
            "full_name": r["full_name"],
            "name": r["name"],
            "owner": r["owner"]["login"],
            "private": r["private"],
            "description": r.get("description"),
            "language": r.get("language"),
            "updated_at": r["updated_at"],
            "connected": r["full_name"] in connected,
        }
        for r in github_repos
        if isinstance(r, dict)
    ]


@router.post("/repos/connect")
async def connect_repo(body: dict, user: dict = Depends(get_current_user)):
    repo_full_name = body.get("repo_full_name")
    if not repo_full_name:
        raise HTTPException(status_code=400, detail="repo_full_name이 필요합니다")

    webhook_url = f"{settings.webhook_base_url}/webhook/github"

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/repos/{repo_full_name}/hooks",
            headers={
                "Authorization": f"Bearer {user['access_token']}",
                "Accept": "application/vnd.github+json",
            },
            json={
                "name": "web",
                "active": True,
                "events": ["pull_request"],
                "config": {
                    "url": webhook_url,
                    "content_type": "json",
                    "secret": settings.github_webhook_secret,
                },
            },
        )
        if response.status_code not in (200, 201):
            raise HTTPException(status_code=502, detail="GitHub webhook 등록에 실패했습니다")
        webhook_id = response.json()["id"]

    async with async_session() as session:
        session.add(Repository(
            user_id=int(user["sub"]),
            repo_full_name=repo_full_name,
            webhook_id=webhook_id,
        ))
        await session.commit()

    return {"connected": True, "repo_full_name": repo_full_name}


@router.delete("/repos/disconnect")
async def disconnect_repo(body: dict, user: dict = Depends(get_current_user)):
    repo_full_name = body.get("repo_full_name")
    if not repo_full_name:
        raise HTTPException(status_code=400, detail="repo_full_name이 필요합니다")

    async with async_session() as session:
        result = await session.execute(
            select(Repository).where(
                Repository.user_id == int(user["sub"]),
                Repository.repo_full_name == repo_full_name,
            )
        )
        repo = result.scalar_one_or_none()
        if repo is None:
            raise HTTPException(status_code=404, detail="연동된 저장소를 찾을 수 없습니다")

        async with httpx.AsyncClient() as client:
            await client.delete(
                f"https://api.github.com/repos/{repo_full_name}/hooks/{repo.webhook_id}",
                headers={
                    "Authorization": f"Bearer {settings.github_bot_token}",
                    "Accept": "application/vnd.github+json",
                },
            )

        await session.execute(
            delete(Repository).where(Repository.id == repo.id)
        )
        await session.commit()

    return {"connected": False, "repo_full_name": repo_full_name}
