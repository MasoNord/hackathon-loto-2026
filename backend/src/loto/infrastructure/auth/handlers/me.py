import decimal
from dataclasses import dataclass
from uuid import UUID

from loto.domain.vo.role import Role
from loto.infrastructure.persistence_sqla import Users



@dataclass
class BankAccountRead:
    id: UUID
    balance: decimal.Decimal

@dataclass
class UserReadMe:
    id: UUID
    username: str
    role: Role
    avatar: str
    bank_account: BankAccountRead

class Me:
    async def execute(self, user: Users) -> UserReadMe:
        return UserReadMe(
            id=user.id,
            username=user.username,
            role=Role(user.role.name),
            avatar=user.avatar_url,
            bank_account=BankAccountRead(
                id=user.bank_account.id,
                balance=user.bank_account.balance
            )
        )