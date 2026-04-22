from dataclasses import dataclass
import uuid

import uuid6
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from loto.infrastructure.persistence_sqla.base import Base


@dataclass
class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7()
    )
    username: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=True)
    bank_account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bank_account.id", ondelete="SET NULL"))
    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="SET NULL"))

    bank_account: Mapped["BankAccount"] = relationship(back_populates="user")
    role: Mapped["Roles"] = relationship(back_populates="user")
    created_rooms = relationship(
        "Room",
        back_populates="creator"
    )