import uuid

import uuid6
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped, mapped_column

from loto.infrastructure.persistence_sqla.base import Base


class UserBalanceChange(Base):

    __tablename__ = "user_balance_changes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7()
    )

    room_win_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("room_wins.id", ondelete="CASCADE"))
    withdraw_history_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bank_account_withdraw_history.id", ondelete="CASCADE"))
