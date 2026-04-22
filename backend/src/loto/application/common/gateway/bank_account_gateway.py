from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loto.infrastructure.persistence_sqla import BankAccount


class BankAccountGateway(Protocol):

    @abstractmethod
    async def withdraw(self, bank_account: BankAccount) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, bank_account_id: UUID) -> BankAccount | None:
        raise NotImplementedError

    @abstractmethod
    async def add(self, bank_account: BankAccount) -> None:
        raise NotImplementedError