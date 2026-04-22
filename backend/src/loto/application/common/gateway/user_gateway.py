from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loto.infrastructure.persistence_sqla import Users


class UserGateway(Protocol):
    @abstractmethod
    async def add(self, user: Users) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Users | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> Users | None:
        raise NotImplementedError