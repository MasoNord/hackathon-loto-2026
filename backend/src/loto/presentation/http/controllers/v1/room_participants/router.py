from fastapi import APIRouter

from loto.presentation.http.controllers.v1.room_participants.join import create_join_room_router

def create_room_participants_router() -> APIRouter:
    router = APIRouter(prefix="/room-participants", tags=["Room Participants Specific"])

    router.include_router(create_join_room_router())

    return router