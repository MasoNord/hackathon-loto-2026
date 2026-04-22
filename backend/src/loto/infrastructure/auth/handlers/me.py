import decimal
import logging
from dataclasses import dataclass
from uuid import UUID

from loto.domain.vo.role import Role
from loto.infrastructure.persistence_sqla import BankAccount, Users

logger = logging.getLogger(__name__)


@dataclass
class BankAccountRead:
    id: UUID
    balance: decimal.Decimal

@dataclass
class UserReadMe:
    id: UUID
    first_name: str
    last_name: str
    middle_name: str
    email: str
    role: Role
    bank_account: BankAccountRead


class Me:
    async def execute(self, user: Users) -> UserReadMe:
        return UserReadMe(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            middle_name=user.middle_name,
            email=user.email,
            role=Role(user.role.name),
            bank_account=BankAccountRead(
                id=user.bank_account.id,
                balance=user.bank_account.balance
            )
        )