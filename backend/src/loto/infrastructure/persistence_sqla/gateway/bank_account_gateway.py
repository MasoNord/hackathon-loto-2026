from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from loto.application.common.gateway.bank_account_gateway import BankAccountGateway
from loto.infrastructure.adapters.types import MainAsyncSession
from loto.infrastructure.exceptions.base import InfrastructureError
from loto.infrastructure.persistence_sqla import BankAccount


class SABankAccountGateway(BankAccountGateway):

    def __init__(self, session: MainAsyncSession):
        self._session = session


    async def withdraw(self, bank_account: BankAccount) -> None:
        pass

    async def get_by_id(self, bank_account_id: UUID) -> BankAccount | None:
        stmt = select(BankAccount).filter_by(id=bank_account_id)

        record = await self._session.execute(stmt)

        result = record.scalar_one_or_none()

        return result

    async def add(self, bank_account: BankAccount) -> None:
        try:
            self._session.add(bank_account)
            await self._session.flush((bank_account,))
        except SQLAlchemyError as e:
            raise InfrastructureError from e