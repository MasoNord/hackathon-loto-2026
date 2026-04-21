import logging
import redis.asyncio as aioredis
from typing import AsyncIterator, cast
from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from loto.bootstrap.config.database import LocalDBConnectionConfig, EngineSettings
from loto.bootstrap.config.redis import RedisConfig
from loto.infrastructure.adapters.types import MainAsyncSession, MainAsyncRedisPool, MainAsyncRedisConnection

logger = logging.getLogger(__name__)

class LocalDatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_async_engine(
        self,
        postgres: LocalDBConnectionConfig,
        engine_settings: EngineSettings
    ) -> AsyncIterator[AsyncEngine]:
        async_engine = create_async_engine(
            url=postgres.postgres_conn_url,
            echo=engine_settings.echo,
            echo_pool=engine_settings.echo_pool,
            pool_size=engine_settings.pool_size,
            max_overflow=engine_settings.max_overflow,
            connect_args={"timeout": 5},
            pool_pre_ping=True
        )

        logger.debug("Local async engine created with DSN %s", postgres.postgres_conn_url)
        yield async_engine
        logger.debug("Disposing async engine...")
        await async_engine.dispose()
        logger.debug("Engine is disposed")

    @provide(scope=Scope.APP)
    def provide_async_session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        async_session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False
        )
        logger.debug("Async session maker initialized")
        return async_session_factory

    @provide(scope=Scope.REQUEST)
    async def provide_main_async_session(
        self,
        async_session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[MainAsyncSession]:

        logger.debug("Starting Main async session...")
        async with async_session_factory() as session:
            logger.debug("Main async session started.")
            yield cast(MainAsyncSession, session)
            logger.debug("Closing Main async session.")
        logger.debug("Main async session closed.")

class LocalRedisProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_async_redis_pool(self, redis_config: RedisConfig) -> AsyncIterator[MainAsyncRedisPool]:

        pool = aioredis.ConnectionPool.from_url(
            redis_config.redis_conn_url,
            max_connections=redis_config.max_connections,
            decode_responses=redis_config.decode_response,
        )

        logger.debug("Local async redis pool started...")
        yield cast(MainAsyncRedisPool, pool)
        logger.debug("Local async redis pool closing...")
        await pool.disconnect()
        logger.debug("Local async redis pool is closed!")

    @provide(scope=Scope.REQUEST)
    async def provide_async_redis_connection(self, local_redis_pool: MainAsyncRedisPool) -> AsyncIterator[MainAsyncRedisConnection]:
        logger.debug("Starting Local redis connection...")
        redis_client = aioredis.Redis(connection_pool=local_redis_pool)

        yield cast(MainAsyncRedisConnection, redis_client)
        logger.debug("Closing local redis connection...")
        await redis_client.close()
        logger.debug("Local redis connection is closed...")


def infrastructure_providers() -> tuple[Provider, ...]:
    return (
        LocalRedisProvider(),
        LocalDatabaseProvider()
    )