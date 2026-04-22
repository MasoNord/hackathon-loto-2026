from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_200_OK
from loto.application.common.services.current_user import CurrentUserService
from loto.application.room.read import ReadRooms, ReadRoomByID


def create_read_rooms() -> APIRouter:
    router = APIRouter()

    @router.get(
        "/",
        status_code=HTTP_200_OK
    )
    @inject
    async def read_rooms(
        interactor: FromDishka[ReadRooms],
        current_user_service: FromDishka[CurrentUserService]
    ):
        current_user = await current_user_service.get_current_user()

        return await interactor.execute(current_user)

    return router

def create_read_room() -> APIRouter:
    router = APIRouter()

    @router.get(
        "/{room_id:int}",
        status_code=HTTP_200_OK
    )
    @inject
    async def read_room_by_id(
        interactor: FromDishka[ReadRoomByID],
        current_user_service: FromDishka[CurrentUserService],
        room_id: int
    ):
        current_user = await current_user_service.get_current_user()
        return await interactor.execute(room_id, current_user)

    return router