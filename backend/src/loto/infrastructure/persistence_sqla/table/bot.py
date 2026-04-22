import uuid

import uuid6
from sqlalchemy import String

from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped, mapped_column
from loto.infrastructure.persistence_sqla.base import Base


class Bot(Base):
    __tablename__ = "bots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7()
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)