import uuid

import uuid6
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped, mapped_column

from loto.infrastructure.persistence_sqla.base import Base


class RoomWin(Base):

    __tablename__ = "room_wins"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7()
    )

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    bot_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bots.id", ondelete="CASCADE"), nullable=True)
    user_count: Mapped[int] = mapped_column(Integer, nullable=False)
    bot_count: Mapped[int] = mapped_column(Integer, nullable=False)
    boosts: Mapped[int] = mapped_column(Integer, nullable=False)