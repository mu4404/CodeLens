import hashlib
import hmac

from fastapi import APIRouter, Header, HTTPException, Request

from app.core.config import settings

router = APIRouter()


@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None),
):
    body = await request.body()
    expected_signature = "sha256=" + hmac.new(
        settings.github_webhook_secret.encode(), body, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, x_hub_signature_256 or ""):
        raise HTTPException(status_code=401, detail="유효하지 않은 서명입니다.")

    payload = await request.json()

    if x_github_event == "pull_request" and payload.get("action") in ("opened", "synchronize"):
        print(f"PR #{payload['number']} {payload['action']} - {payload['pull_request']['title']}")

    return {"status": "received"}
