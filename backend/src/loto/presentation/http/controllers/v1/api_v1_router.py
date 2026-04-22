from fastapi import APIRouter

from loto.presentation.http.controllers.v1.account.router import create_account_router
from loto.presentation.http.controllers.v1.general.router import create_general_router
from loto.presentation.http.controllers.v1.room.router import create_room_router
from loto.presentation.http.controllers.v1.room_participants.router import create_room_participants_router
from loto.presentation.http.controllers.v1.user.router import create_user_router


def create_api_v1_router() -> APIRouter:
    router = APIRouter(prefix="/api/v1")

    router.include_router(create_general_router())
    router.include_router(create_account_router())
    router.include_router(create_room_router())
    router.include_router(create_room_participants_router())
    router.include_router(create_user_router())

    return router