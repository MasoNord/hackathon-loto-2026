import decimal
import uuid

import uuid6
from sqlalchemy import ForeignKey, Boolean, DECIMAL
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from loto.infrastructure.persistence_sqla.base import Base


class RoomParticipant(Base):
    __tablename__ = "room_participants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7()
    )

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    boot_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bots.id"), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=True)

    is_boosted: Mapped[bool] = mapped_column(Boolean, nullable=False)

    reserved_balance: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18,2), nullable=False)

    room: Mapped["Room"] = relationship(backref="room_participants")
