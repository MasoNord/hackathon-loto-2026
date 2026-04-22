from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from loto.application.common.services.current_user import CurrentUserService
from loto.application.room.read import ReadRooms


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