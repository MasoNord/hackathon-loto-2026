from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RedisConfig:
    max_connections: int
    port: int
    host: str
    decode_response: bool
    password: str
    username: str

    @property
    def redis_conn_url(self) -> str:
        return f"redis://{self.username}:{self.password}@{self.host}:{self.port}"