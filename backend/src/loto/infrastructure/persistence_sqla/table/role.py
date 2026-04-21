import uuid
from dataclasses import dataclass

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
import uuid6
from sqlalchemy.orm import mapped_column, Mapped, relationship
from loto.infrastructure.persistence_sqla.base import Base


@dataclass
class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7()
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)

    user: Mapped["Users"] = relationship(back_populates="role")
