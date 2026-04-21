from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AuthConfig:
    secret_key: str
    session_ttl_min: int
    session_refresh_threshold: float

@dataclass(frozen=True, slots=True)
class CookiesConfig:
    secure: bool

@dataclass(frozen=True, slots=True)
class PasswordConfig:
    time_cost: int
    memory_cost: int
    parallelism: int
    hash_len: int
    salt_len: int