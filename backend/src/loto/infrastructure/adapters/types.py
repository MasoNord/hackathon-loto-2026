import redis.asyncio as aioredis
from typing import NewType
from sqlalchemy.ext.asyncio import AsyncSession

MainAsyncSession = NewType("MainAsyncSession", AsyncSession)
MainAsyncRedisConnection = NewType("MainAsyncRedisConnection", aioredis.Redis)
MainAsyncRedisPool = NewType("MainAsyncRedisPool", aioredis.ConnectionPool)