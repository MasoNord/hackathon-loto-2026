import decimal
import uuid
from typing import List

from sqlalchemy import Integer, String, DECIMAL, text, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from loto.infrastructure.persistence_sqla.base import Base


class Room(Base):
    __tablename__ = "rooms"

    __table_args__ = (
        UniqueConstraint(
            "creator_id",
            "name",
            name="uix_name_creator_room"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    enter_price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 2), nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)

    boosted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("False"))
    boost_price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 2), nullable=False)
    prize_percentage: Mapped[float] = mapped_column(DECIMAL(3, 2), nullable=False)

    creator_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    creator: Mapped["Users"] = relationship(
        "Users",
        back_populates="created_rooms"
    )

    room_participants: Mapped[List["RoomParticipant"]] = relationship(
        "RoomParticipant",
        back_populates="room"
    )