from sqlalchemy.exc import SQLAlchemyError

from loto.application.common.gateway.room_gateway import RoomGateway
from loto.infrastructure.adapters.types import MainAsyncSession
from loto.infrastructure.exceptions.base import InfrastructureError
from loto.infrastructure.persistence_sqla import Room

class SARoomGateway(RoomGateway):

    def __init__(self, session: MainAsyncSession):
        self._session = session

    async def add(self, room: Room) -> None:
        try:
            self._session.add(room)
            await self._session.flush((room,))
        except SQLAlchemyError:
            raise InfrastructureError