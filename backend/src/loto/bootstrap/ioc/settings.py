from dishka import Provider, Scope, provide

from loto.bootstrap.config.application import ApplicationConfig
from loto.bootstrap.config.database import LocalDBConnectionConfig, EngineSettings
from loto.bootstrap.config.redis import RedisConfig
from loto.bootstrap.config.security import AuthConfig, CookiesConfig, PasswordConfig
from loto.infrastructure.config_loader import Config

class SettingsProvider(Provider):
    scope = Scope.APP

    @provide
    def config(self) -> Config:
        return Config.load_from_environment()

    @provide
    def local_db_connection(self, config: Config) -> LocalDBConnectionConfig:
        return config.db_connection

    @provide
    def auth(self, config: Config) -> AuthConfig:
        return config.auth_config

    @provide
    def cookie_config(self, config: Config) -> CookiesConfig:
        return config.cookies_config

    @provide
    def app(self, config: Config) -> ApplicationConfig:
        return config.application_config

    @provide
    def engine_settings(self, config: Config) -> EngineSettings:
        return config.engine_settings

    @provide
    def password_config(self, config: Config) -> PasswordConfig:
        return config.password_config

    @provide
    def redis_config(self, config: Config) -> RedisConfig:
        return config.redis_config