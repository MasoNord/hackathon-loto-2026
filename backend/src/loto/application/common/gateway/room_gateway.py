from abc import abstractmethod
from typing import Protocol

from loto.infrastructure.persistence_sqla import Room


class RoomGateway(Protocol):

    @abstractmethod
    async def add(self, room: Room) -> None:
        raise NotImplementedError