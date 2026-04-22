import uuid6
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from loto.presentation.websockets.connections.connection_manager import ConnectionManager

def create_websocket(app: FastAPI):

    @app.websocket("/ws")
    @inject
    async def websocket_endpoint(
        websocket: WebSocket,
        connection_manager: FromDishka[ConnectionManager]
    ) -> None:
        user_id = websocket.query_params.get("user_id", str(uuid6.uuid7()))
        connection_id = str(uuid6.uuid7())

        await connection_manager.connect(websocket, connection_id, user_id)
        try:
            while True:
                data = await websocket.receive_json()

                event_type = data.get("type")

                if event_type == "join_room":
                    room_id = data["room_id"]

                    await connection_manager.join_room(connection_id, room_id)

                    await connection_manager.broadcast_room_state(room_id)

                if event_type == "room_status":
                    room_id = data["room_id"]
                    await connection_manager.broadcast_room_state(room_id)

        except WebSocketDisconnect:
            room_id = connection_manager.disconnect(connection_id)

            if room_id:
                await connection_manager.broadcast_room_state(room_id)


            pass
