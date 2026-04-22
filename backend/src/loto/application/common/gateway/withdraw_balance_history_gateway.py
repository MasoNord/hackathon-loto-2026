from abc import abstractmethod
from typing import Protocol

from loto.infrastructure.persistence_sqla import BankAccountWithdrawHistory


class WithdrawBalanceHistoryGateway(Protocol):

    @abstractmethod
    async def add(self, bank_account_withdraw_history: BankAccountWithdrawHistory) -> None:
        raise NotImplementedError