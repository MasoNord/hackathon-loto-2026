from enum import StrEnum


class RoomStatus(StrEnum):
    IDLE = "idle"
    WAITING = "waiting"
    PLAYING = "playing"
    FINISHED = "finished"