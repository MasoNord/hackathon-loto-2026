import datetime
import decimal
import logging
import uuid
from dataclasses import dataclass
from datetime import timezone

import uuid6

from loto.application.common.gateway.bank_account_gateway import BankAccountGateway
from loto.application.common.gateway.withdraw_balance_history_gateway import WithdrawBalanceHistoryGateway
from loto.application.common.uow import UoW
from loto.application.exceptions.user import BankAccountNotFoundError
from loto.infrastructure.persistence_sqla import Users, BankAccountWithdrawHistory, BankAccount

logger = logging.getLogger(__name__)

@dataclass
class BankAccountWithdrawRequest:
    money: decimal.Decimal
    bank_account_id: uuid.UUID

class BankAccountWithDraw:

    def __init__(
            self,
            uow: UoW,
            bank_account_gateway: BankAccountGateway,
            withdraw_balance_history_gateway: WithdrawBalanceHistoryGateway
    ):
        self._main_uow = uow
        self._bank_account_gateway = bank_account_gateway
        self._withdraw_balance_history_gateway=withdraw_balance_history_gateway

    async def execute(self, user: Users, withdraw_request: BankAccountWithdrawRequest) -> BankAccount:
        logging.info("Bank account withdraw started. User ID: %s", user.id)

        bank_account = await self._bank_account_gateway.get_by_id(withdraw_request.bank_account_id)

        if not bank_account:
            logger.warning("Bank account now found by ID: %s", withdraw_request.bank_account_id)
            raise BankAccountNotFoundError

        logger.info("Bank account withdraw started. Bank Account ID: %s", withdraw_request.bank_account_id)

        balance_before = bank_account.balance
        balance_after = bank_account.withdraw_money(withdraw_request.money)

        logger.debug("Bank balance before: %s", balance_before)
        logger.debug("Bank balance after: %s", balance_after)

        logger.info("Bank account withdraw ended")

        bank_account_wh = BankAccountWithdrawHistory(
            id = uuid6.uuid7(),
            balance_before = balance_before,
            balance_after = balance_after,
            withdraw_date=datetime.datetime.now(tz=timezone.utc),
            bank_account_id=bank_account.id
        )

        async with self._main_uow:
            await self._withdraw_balance_history_gateway.add(bank_account_wh)
            await self._main_uow.commit()

        return bank_account




