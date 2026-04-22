from fastapi import APIRouter

from loto.presentation.http.controllers.v1.room.create import create_add_room
from loto.presentation.http.controllers.v1.room.read import create_read_rooms, create_read_room


def create_room_router() -> APIRouter:
    router = APIRouter(prefix="/room", tags=["Room specific"])

    router.include_router(create_add_room())
    router.include_router(create_read_rooms())
    router.include_router(create_read_room())

    return router