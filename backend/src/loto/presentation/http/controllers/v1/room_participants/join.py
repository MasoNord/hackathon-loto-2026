from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.status import HTTP_200_OK

from loto.application.common.services.current_user import CurrentUserService
from loto.application.room_participants.join import JoinRoomRequest, JoinRoom


class JoinRoomRequestPydantic(BaseModel):
    is_boosted: bool

def create_join_room_router() -> APIRouter:
    router = APIRouter()

    @router.post(
        "/{room_id:int}",
        status_code=HTTP_200_OK
    )
    @inject
    async def join_room(
        interactor: FromDishka[JoinRoom],
        current_user_service: FromDishka[CurrentUserService],
        room_id: int,
        request_pydantic: JoinRoomRequestPydantic
    ):
        current_user = await current_user_service.get_current_user()

        join_room_request = JoinRoomRequest(
            room_id=room_id,
            is_boosted=request_pydantic.is_boosted
        )

        await interactor.execute(current_user, join_room_request)

    return router