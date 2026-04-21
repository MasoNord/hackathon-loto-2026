import json
from dataclasses import asdict
from datetime import datetime, timezone
from uuid import UUID

from redis.exceptions import RedisError

from loto.infrastructure.adapters.types import MainAsyncRedisConnection
from loto.infrastructure.auth.session.gateway.auth_session import AuthSessionGateway
from loto.infrastructure.auth.session.model import AuthSession
from loto.infrastructure.exceptions.base import InfrastructureError

USER_SESSION_KEY="session:"


class RedisAuthSessionGateway(AuthSessionGateway):

    def __init__(self, redis_connection: MainAsyncRedisConnection):
        self._redis_connection = redis_connection

    async def add(self, auth_session: AuthSession) -> None:
        session_key = f"session:{auth_session.id_}"
        user_sessions_key = f"user:sessions:{str(auth_session.user_id)}"

        ttl = int((auth_session.expiration - datetime.now(timezone.utc)).total_seconds())

        await self._redis_connection.set(
            name=session_key,
            value=json.dumps(asdict(auth_session), default=str),
            ex=ttl
        )

        await self._redis_connection.sadd(user_sessions_key, auth_session.id_)
        await self._redis_connection.expire(user_sessions_key, ttl)

    async def get_by_id(self, auth_session_id: str) -> AuthSession | None:
        session_key = f"session:{auth_session_id}"

        data = await self._redis_connection.get(session_key)

        if not data:
            return None
        json_data = json.loads(data)
        return AuthSession(
            id_=json_data["id_"],
            user_id=json_data["user_id"],
            expiration=datetime.fromisoformat(json_data["expiration"]),
            agent=json_data.get("agent", None),
            ip_address=json_data.get("ip_address", None)
        )

    async def update(self, auth_session: AuthSession) -> None:
        try:
            await self.add(auth_session)
        except RedisError as err:
            raise InfrastructureError from err

    async def delete(self, auth_session_id: str) -> None:
        session_key = f"session:{auth_session_id}"

        auth_session = await self.get_by_id(auth_session_id)

        if not auth_session:
            return

        user_sessions_key = f"user:sessions:{auth_session.user_id}"

        try:
            await self._redis_connection.delete(session_key)
            await self._redis_connection.delete(user_sessions_key)
        except RedisError as err:
            raise InfrastructureError from err

    async def delete_all_for_user(self, user_id: UUID) -> None:
        user_sessions_key = f"user:sessions:{user_id}"

        session_ids = await self._redis_connection.smembers(user_sessions_key)

        if not session_ids:
            return

        session_ids = [sid.decode() if isinstance(sid, bytes) else sid for sid in session_ids]

        session_keys = [f"session:{sid}" for sid in session_ids]

        if session_keys:
            await self._redis_connection.delete(*session_keys)

        await self._redis_connection.delete(user_sessions_key)