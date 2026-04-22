import datetime
import decimal
from dataclasses import dataclass
from typing import Tuple

import uuid6

from loto.application.common.gateway.bank_account_gateway import BankAccountGateway
from loto.application.common.gateway.room_gateway import RoomGateway
from loto.application.common.gateway.room_participants_gateway import RoomParticipantsGateway
from loto.application.common.gateway.withdraw_balance_history_gateway import WithdrawBalanceHistoryGateway
from loto.application.common.uow import UoW
from loto.application.exceptions.room import RoomNotFoundError
from loto.application.exceptions.room_participants import NotEnoughMoneyError
from loto.domain.vo.withdraw_type import WithdrawType
from loto.infrastructure.persistence_sqla import Users, BankAccount, BankAccountWithdrawHistory, RoomParticipant


@dataclass
class JoinRoomRequest:
    room_id: int
    is_boosted: bool

class JoinRoom:

    def __init__(
            self,
            uow: UoW,
            room_participant_gateway: RoomParticipantsGateway,
            bank_account_gateway: BankAccountGateway,
            room_gateway: RoomGateway,
            bank_account_withdraw_history: WithdrawBalanceHistoryGateway
    ):
        self._room_participant_gateway = room_participant_gateway
        self._bank_account_withdraw_history = bank_account_withdraw_history
        self._bank_account_gateway = bank_account_gateway
        self._room_gateway = room_gateway
        self._main_uow = uow

    async def execute(self, user: Users, join_room_request: JoinRoomRequest) -> None:
        room = await self._room_gateway.get_by_id(join_room_request.room_id)

        if not room:
            raise RoomNotFoundError

        balance_before = user.bank_account.balance
        charged_price, balance_after = self._charge_user_bank_account(
            user.bank_account,
            join_room_request.is_boosted,
            room.enter_price,
            room.boost_price
        )

        bank_account_wh = BankAccountWithdrawHistory(
            id=uuid6.uuid7(),
            type=WithdrawType.ENTER_ROOM_PAY,
            balance_before=balance_before,
            balance_after=balance_after,
            bank_account_id=user.bank_account_id,
            withdraw_date=datetime.datetime.now(tz=datetime.timezone.utc)
        )

        room_participant = RoomParticipant(
            id=uuid6.uuid7(),
            room_id=join_room_request.room_id,
            user_id=user.id,
            is_boosted=join_room_request.is_boosted,
            reserved_balance=charged_price
        )


        async with self._main_uow:
            await self._room_participant_gateway.add(room_participant)
            await self._bank_account_withdraw_history.add(bank_account_wh)
            await self._main_uow.commit()

        return None

    def _charge_user_bank_account(
        self,
        bank_account: BankAccount,
        is_boosted: bool,
        enter_price: decimal.Decimal,
        price_per_boost: decimal.Decimal
    ) -> Tuple[decimal.Decimal, decimal.Decimal]:
        """
        Calculate the total price to enter the room and charge user's money
        :param bank_account:
        :param is_boosted:
        :param enter_price:
        :param price_per_boost:
        :return: charged price and left bank's balance after enter room charge
        """

        total_price = enter_price

        if is_boosted:
            total_price += price_per_boost

        if bank_account.balance < total_price:
            raise NotEnoughMoneyError

        return total_price, bank_account.charge_moeny(total_price)




