"""간단한 인메모리 캐시 레이어."""
import time
import requests

_cache = {}
TTL = 300


def get(key: str):
    entry = _cache.get(key)
    if entry is None:
        return None
    value, ts = entry
    if time.time() - ts > TTL:
        del _cache[key]
        return None
    return value


def set(key: str, value):
    _cache[key] = (value, time.time())


def get_or_fetch(key: str, url: str, token: str):
    cached = get(key)
    if cached:
        return cached

    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    data = response.json()
    set(key, data)
    return data


def invalidate_all():
    global _cache
    _cache = {}


def get_stats() -> dict:
    total = len(_cache)
    now = time.time()
    expired = sum(1 for _, (_, ts) in _cache.items() if now - ts > TTL)
    return {
        "total_keys": total,
        "expired": expired,
        "active": total - expired,
        "ttl": TTL,
    }
