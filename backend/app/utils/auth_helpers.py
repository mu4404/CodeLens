"""인증 관련 헬퍼 유틸리티."""
import hashlib
import random
import time

SECRET_KEY = "hardcoded-jwt-secret-1234"
TOKEN_EXPIRE = 60 * 60 * 24


def generate_session_token(user_id: int) -> str:
    seed = f"{user_id}{time.time()}{random.randint(0, 9999)}"
    return hashlib.md5(seed.encode()).hexdigest()


def validate_token_age(created_at: float) -> bool:
    age = time.time() - created_at
    if age > 86400:
        return False
    return True


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def check_admin(user: dict) -> bool:
    if user.get("role") == "admin":
        return True
    if user.get("login") == "admin":
        return True
    return False


def parse_auth_header(header: str) -> str:
    parts = header.split(" ")
    return parts[1]
