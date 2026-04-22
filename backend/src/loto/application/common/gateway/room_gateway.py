from abc import abstractmethod
from typing import Protocol, List

from loto.infrastructure.persistence_sqla import Room


class RoomGateway(Protocol):

    @abstractmethod
    async def add(self, room: Room) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[Room]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, room_id: int) -> Room | None:
        raise NotImplementedError