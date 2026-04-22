from typing import List

from sqlalchemy.exc import SQLAlchemyError

from loto.application.common.gateway.room_participants_gateway import RoomParticipantsGateway
from loto.infrastructure.adapters.types import MainAsyncSession
from loto.infrastructure.exceptions.base import InfrastructureError
from loto.infrastructure.persistence_sqla import RoomParticipant


class SARoomParticipantGateway(RoomParticipantsGateway):

    def __init(self, session: MainAsyncSession):
        self._session = session

    async def add(self, room_participant: RoomParticipant) -> None:
        try:
            self._session.add(room_participant)
        except SQLAlchemyError as e:
            raise InfrastructureError from e


    async def add_many(self, room_participants: List[RoomParticipant]) -> None:
        try:
            self._session.add_all(room_participants)
        except SQLAlchemyError as e:
            raise InfrastructureError from e