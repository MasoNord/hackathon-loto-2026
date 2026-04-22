import decimal
import logging
from dataclasses import dataclass

from loto.application.common.gateway.room_gateway import RoomGateway
from loto.application.common.uow import UoW
from loto.infrastructure.persistence_sqla import Room, Users


logger = logging.getLogger(__name__)

@dataclass
class CreateRoomRequest:
    name: str
    enter_price: decimal.Decimal
    seats: int
    boosted: bool
    boost_price: int
    prize_percentage: decimal.Decimal

class CreateRoom:

    def __init__(self, room_gateway: RoomGateway, uow: UoW):
        self._room_gateway = room_gateway
        self._main_uow = uow


    async def execute(self, create_request: CreateRoomRequest, user: Users) -> None:

        logger.info("Room creation started: User ID: %s", user.id)

        room = Room(
            name=create_request.name,
            enter_price=create_request.enter_price,
            seats=create_request.seats,
            boosted=create_request.boosted,
            boost_price=create_request.boost_price,
            prize_percentage=create_request.prize_percentage,
            creator_id = user.id
        )

        async with self._main_uow:
            await self._room_gateway.add(room)
            await self._main_uow.commit()

        logger.info("Room creation ended")