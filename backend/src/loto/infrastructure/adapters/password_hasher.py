from loto.bootstrap.config.security import PasswordConfig
from loto.domain.gateway.password_hasher import PasswordHasher
from argon2 import PasswordHasher as ArgonPasswordHasherLib


class ArgonPasswordHasher(PasswordHasher):

    def __init__(self, config: PasswordConfig):
        self._ph = ArgonPasswordHasherLib (
            time_cost=config.time_cost,
            memory_cost=config.memory_cost,
            parallelism=config.parallelism,
            hash_len=config.hash_len,
            salt_len=config.salt_len
        )
        self.config = config

    async def hash(self, raw_password: bytes) -> bytes:
        hashed_password = self._ph.hash(
            password=raw_password
        )

        return hashed_password.encode("utf-8")

    async def verify(self, raw_password: bytes, hashed_password: bytes) -> bool:
        return self._ph.verify(
            hashed_password, raw_password)
