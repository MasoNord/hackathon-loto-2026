from abc import abstractmethod
from typing import Protocol, List

from loto.infrastructure.persistence_sqla import RoomParticipant


class RoomParticipantsGateway(Protocol):

    @abstractmethod
    async def add(self, room_participant: RoomParticipant) -> None:
        raise NotImplementedError

    @abstractmethod
    async def add_many(self, room_participants: List[RoomParticipant]) -> None:
        raise NotImplementedError