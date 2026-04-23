import logging
from typing import Dict, Set

from starlette.websockets import WebSocket

from loto.presentation.websockets.connections.gateway.connection_manager import ConnectionManager

logger = logging.getLogger(__name__)

class FastApiConnectionManager(ConnectionManager):
    def __init__(self):
        self.rooms: Dict[int, Set[str]] = {}
        self.connections: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, connection_id: str, user_id: str):
        logger.info("Start connection to a websocket: connection_id: %s, user_id: %s", connection_id, user_id)

        await websocket.accept()

        self.connections[connection_id] = {
            "ws": websocket,
            "user_id": user_id,
            "room_id": None,
        }

        logger.info("Connection to a websocket ended successfully")

    def disconnect(self, connection_id: str):
        conn = self.connections.get(connection_id)
        if not conn:
            return None

        room_id = conn["room_id"]

        if room_id and room_id in self.rooms:
            self.rooms[room_id].discard(connection_id)

        del self.connections[connection_id]

        return room_id

    async def join_room(self, connection_id: str, room_id: int):
        conn = self.connections[connection_id]

        old_room = conn["room_id"]
        if old_room and old_room in self.rooms:
            self.rooms[old_room].discard(connection_id)

        conn["room_id"] = room_id

        if room_id not in self.rooms:
            self.rooms[room_id] = set()

        self.rooms[room_id].add(connection_id)

    async def broadcast_room_state(self, room_id: int):
        cids = self.rooms.get(room_id, set())

        users = [
            self.connections[cid]["user_id"]
            for cid in cids
        ]

        payload = {
            "type": "room_state",
            "count": len(users),
            "users": users,
        }

        for cid in cids:
            ws: WebSocket = self.connections[cid]["ws"]
            await ws.send_json(payload)