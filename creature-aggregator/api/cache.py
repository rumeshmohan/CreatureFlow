import aioredis
from fastapi_limiter import FastAPILimiter
import os

REDIS_URL = os.getenv("REDIS_URL")
redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

async def init_redis():
    await FastAPILimiter.init(redis)
