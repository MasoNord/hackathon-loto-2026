from abc import abstractmethod
from typing import Protocol

from loto.infrastructure.persistence_sqla import BankAccount


class BankAccountGateway(Protocol):

    @abstractmethod
    async def add(self, bank_account: BankAccount) -> None:
        raise NotImplementedError

