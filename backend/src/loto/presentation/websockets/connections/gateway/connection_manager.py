from abc import abstractmethod
from typing import Protocol

from starlette.websockets import WebSocket


class ConnectionManager(Protocol):

    @abstractmethod
    async def connect(self, websocket: WebSocket, connection_id: str, user_id: str):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, connection_id: str):
        raise NotImplementedError

    @abstractmethod
    async def join_room(self, connection_id: str, room_id: int):
        raise NotImplementedError

    @abstractmethod
    async def broadcast_room_state(self, room_id: int):
        raise NotImplementedError