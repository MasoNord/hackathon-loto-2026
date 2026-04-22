import decimal

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette.status import HTTP_201_CREATED

from loto.application.common.services.current_user import CurrentUserService
from loto.application.room.create import CreateRoom, CreateRoomRequest


class CreateRoomRequestPydantic(BaseModel):
    name: str = Field(max_length=255)
    enter_price: decimal.Decimal
    seats: int
    boosted: bool
    boost_price: int
    prize_percentage: decimal.Decimal

def create_add_room() -> APIRouter:
    router = APIRouter()

    @router.post(
        "/",
        status_code = HTTP_201_CREATED
    )
    @inject
    async def create_room(
        interactor: FromDishka[CreateRoom],
        current_user_service: FromDishka[CurrentUserService],
        request_data: CreateRoomRequestPydantic
    ):

        current_user = await current_user_service.get_current_user()

        create_room_request = CreateRoomRequest(
            name=request_data.name,
            enter_price=request_data.enter_price,
            seats=request_data.seats,
            boosted=request_data.boosted,
            boost_price=request_data.boost_price,
            prize_percentage=request_data.prize_percentage
        )

        await interactor.execute(create_room_request, current_user)

    return router