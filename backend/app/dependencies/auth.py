import jwt

from fastapi import Cookie, HTTPException

from app.core.config import settings


def get_current_user(access_token: str | None = Cookie(default=None)):
    if access_token is None:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    
    try:
        payload = jwt.decode(access_token, settings.jwt_secret, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    
    return payload