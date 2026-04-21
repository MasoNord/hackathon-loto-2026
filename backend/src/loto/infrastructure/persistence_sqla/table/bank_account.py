import decimal
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List

import uuid6
from sqlalchemy import DECIMAL, DateTime
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from loto.infrastructure.persistence_sqla.base import Base


@dataclass
class BankAccount(Base):
    __tablename__ = "bank_account"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7()
    )
    balance: Mapped[decimal.Decimal] = mapped_column(
        DECIMAL(18, 2)
    )

    last_withdraw: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["Users"] = relationship(back_populates="bank_account")

    bank_withdraw_histories: Mapped[List["BankAccountWithdrawHistory"]] = relationship(back_populates="bank_account")
