import logging
from dataclasses import dataclass
from typing import List

from loto.application.common.gateway.room_gateway import RoomGateway
from loto.infrastructure.persistence_sqla import Room, Users

logger = logging.getLogger(__name__)

@dataclass
class ReadRoomsFilter:
    name: str

class ReadRooms:

    def __init__(self, room_gateway: RoomGateway):
        self._room_gateway = room_gateway

    async def execute(self, user: Users) -> List[Room]:

        logger.info("Get rooms started: User ID: %s", user.id)

        rooms = await self._room_gateway.get_all()

        logger.info("Get rooms ended: User ID: %s", user.id)

        return rooms

