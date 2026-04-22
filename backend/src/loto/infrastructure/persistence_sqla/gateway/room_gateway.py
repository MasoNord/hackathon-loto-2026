from typing import List

from sqlalchemy import select
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

    async def get_all(self) -> List[Room]:
        try:
            stmt = select(Room)
            records = await self._session.execute(stmt)
            result = records.scalars().all()
        except SQLAlchemyError:
            raise InfrastructureError

        return list(result)

    async def get_by_id(self, room_id: int) -> Room | None:
        stmt = select(Room).filter_by(id = room_id)

        try:
            record = await self._session.execute(stmt)
            result = record.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise InfrastructureError from e

        return result


