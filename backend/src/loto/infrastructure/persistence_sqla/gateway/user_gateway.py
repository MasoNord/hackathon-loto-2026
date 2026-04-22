from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from loto.application.common.gateway.user_gateway import UserGateway
from loto.domain.exceptions.user import EmailAlreadyExistsError
from loto.infrastructure.adapters.types import MainAsyncSession
from loto.infrastructure.exceptions.base import InfrastructureError
from loto.infrastructure.persistence_sqla import Users


class SAUserGateway(UserGateway):

    def __init__(self, session: MainAsyncSession):
        self._session = session

    async def add(self, user: Users) -> None:
        try:
            self._session.add(user)
            await self._session.flush((user,))
        except IntegrityError as e:
            if "ix_users_email" in str(e):
                raise EmailAlreadyExistsError()
            else:
                raise InfrastructureError

    async def get_by_id(self, user_id: UUID) -> Users | None:
        stmt = (select(Users).where(Users.id == user_id)
                .options(selectinload(Users.bank_account))
                .options(selectinload(Users.role))
        )

        record = await self._session.execute(stmt)

        result = record.scalar_one_or_none()

        return result

    async def get_by_username(self, username: str) -> Users | None:
        pass

    async def get_by_email(self, email: str) -> Users | None:
        stmt = select(Users).where(Users.email == email)

        record = await self._session.execute(stmt)

        result = record.scalar_one_or_none()

        return result