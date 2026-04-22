from loto.application.common.gateway.withdraw_balance_history_gateway import WithdrawBalanceHistoryGateway
from loto.infrastructure.persistence_sqla import BankAccountWithdrawHistory


class SAWithdrawBalanceHistoryGateway(WithdrawBalanceHistoryGateway):
    async def add(self, bank_account_withdraw_history: BankAccountWithdrawHistory) -> None:
        pass