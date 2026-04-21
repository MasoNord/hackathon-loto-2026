import decimal
import uuid
from datetime import datetime

import uuid6
from sqlalchemy import String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from loto.infrastructure.persistence_sqla.base import Base


class BankAccountWithdrawHistory(Base):
    __tablename__ = "bank_account_withdraw_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid6.uuid7()
    )

    type: Mapped[str] = mapped_column(String(255), nullable=False)

    balance_before: Mapped[decimal.Decimal] = mapped_column(DECIMAL, nullable=False)
    balance_after: Mapped[decimal.Decimal] = mapped_column(DECIMAL, nullable=False)
    withdraw_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    bank_account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bank_account.id", ondelete="CASCADE"))
    bank_account: Mapped["BankAcount"] = relationship(back_populates="bank_withdraw_histories")