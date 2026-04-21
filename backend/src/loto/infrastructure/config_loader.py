import logging
import os

from dataclasses import dataclass

from loto.bootstrap.config.application import ApplicationConfig
from loto.bootstrap.config.database import LocalDBConnectionConfig, EngineSettings
from loto.bootstrap.config.redis import RedisConfig
from loto.bootstrap.config.security import AuthConfig, PasswordConfig, CookiesConfig

logger = logging.getLogger(__name__)

def to_bool(value: str) -> bool:
    return value.lower() in ("1", "true")

@dataclass
class Config:
    db_connection: LocalDBConnectionConfig
    engine_settings: EngineSettings
    auth_config: AuthConfig
    application_config: ApplicationConfig
    password_config: PasswordConfig
    cookies_config: CookiesConfig
    redis_config: RedisConfig

    @classmethod
    def load_from_environment(cls: type["Config"]) -> "Config":
        db = LocalDBConnectionConfig(
            postgres_username=os.environ["POSTGRES_USERNAME"],
            postgres_password=os.environ["POSTGRES_PASSWORD"],
            postgres_host=os.environ["POSTGRES_HOST"],
            postgres_port=int(os.environ["POSTGRES_PORT"]),
            postgres_database=os.environ["POSTGRES_DATABASE"],
        )
        auth_config = AuthConfig(
            secret_key=os.environ["SECRET_KEY"],
            session_ttl_min=int(os.environ["SESSION_TTL"]),
            session_refresh_threshold=float(os.environ["SESSION_THRESHOLD"])
        )

        engine_settings = EngineSettings(
            echo=to_bool(os.environ["ENGINE_ECHO"]),
            echo_pool=to_bool(os.environ["ENGINE_ECHO_POOL"]),
            pool_size=int(os.environ["ENGINE_POOL_SIZE"]),
            max_overflow=int(os.environ["ENGINE_MAX_OVERFLOW"])
        )

        application = ApplicationConfig(
            host=os.environ["APP_HOST"],
            port=int(os.environ["APP_PORT"]),
            logging_debug=to_bool(os.environ["APP_LOGGING_DEBUG"])
        )

        password_config = PasswordConfig(
            time_cost=int(os.environ["PASSWORD_TIME_COST"]),
            memory_cost=int(os.environ["PASSWORD_MEMORY_COST"]),
            parallelism=int(os.environ["PASSWORD_PARALLELISM"]),
            hash_len=int(os.environ["PASSWORD_HASH_LEN"]),
            salt_len=int(os.environ["PASSWORD_SALT_LEN"])
        )

        cookies_config = CookiesConfig(
            secure=to_bool(os.environ["SESSION_COOKIE_SECURE"])
        )

        redis = RedisConfig(
            max_connections=int(os.environ["REDIS_MAX_CONNECTIONS"]),
            port=int(os.environ["REDIS_PORT"]),
            host=str(os.environ["REDIS_HOST"]),
            decode_response=to_bool(os.environ["REDIS_DECODE_RESPONSE"]),
            username = os.environ["REDIS_ACL_USERNAME"],
            password = os.environ["REDIS_ACL_PASSWORD"]
        )

        logger.debug("Config loaded.")

        return cls(
            db_connection=db,
            engine_settings=engine_settings,
            auth_config=auth_config,
            application_config=application,
            password_config=password_config,
            cookies_config=cookies_config,
            redis_config=redis
        )
