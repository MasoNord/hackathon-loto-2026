from fastapi import APIRouter

from loto.presentation.http.controllers.v1.room.create import create_add_room


def create_room_router() -> APIRouter:
    router = APIRouter(prefix="/room")

    router.include_router(create_add_room())

    return router