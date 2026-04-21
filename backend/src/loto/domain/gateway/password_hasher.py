from abc import abstractmethod
from typing import Protocol


class PasswordHasher(Protocol):
    @abstractmethod
    async def hash(self, raw_password: bytes) -> bytes:
        raise NotImplementedError

    @abstractmethod
    async def verify(
        self,
        raw_password: bytes,
        hashed_password: bytes,
    ) -> bool:
        raise NotImplementedError