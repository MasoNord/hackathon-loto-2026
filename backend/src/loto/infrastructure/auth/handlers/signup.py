import decimal
import logging
from dataclasses import dataclass
from typing import Final
from uuid import UUID

import uuid6

from loto.application.common.gateway.bank_account_gateway import BankAccountGateway
from loto.application.common.gateway.role_gateway import RoleGateway
from loto.application.common.gateway.user_gateway import UserGateway
from loto.application.common.services.avatar_generator import AvatarGenerator
from loto.application.common.services.current_user import CurrentUserService
from loto.application.common.uow import UoW
from loto.application.exceptions.base import ApplicationError
from loto.application.exceptions.uow import CommitError
from loto.domain.exceptions.user import UsernameAlreadyExistsError, EmailAlreadyExistsError
from loto.domain.gateway.password_hasher import PasswordHasher
from loto.domain.vo.role import Role
from loto.infrastructure.exceptions.auth import AlreadyAuthenticatedError, AuthenticationError, PasswordDoesntMatchError
from loto.infrastructure.persistence_sqla import Users, BankAccount

logger = logging.getLogger(__name__)

DEFAULT_USER_BANK_ACCOUNT_BALANCE: Final[decimal.Decimal] = decimal.Decimal("1000.00")

@dataclass(frozen=True, slots=True, kw_only=True)
class SignUpRequest:
    password: str
    repeat_password: str
    username: str
    email: str

@dataclass
class SignUpResponse:
    id: UUID

class SignUp:
    def __init__(
        self,
        current_user_service: CurrentUserService,
        password_hasher: PasswordHasher,
        user_gateway: UserGateway,
        user_role_gateway: RoleGateway,
        bank_account_gateway: BankAccountGateway,
        avatar_generator: AvatarGenerator,
        uow: UoW,
    ):
        self._current_user_service = current_user_service
        self._password_hasher = password_hasher
        self._user_gateway = user_gateway
        self._main_uow = uow
        self._user_role_gateway = user_role_gateway
        self._bank_account_gateway=bank_account_gateway
        self._avatar_generator=avatar_generator

    async def execute(self, request_data: SignUpRequest) -> SignUpResponse:
        logger.info("Sign up: started. Email '%s'", request_data.email)

        try:
            await self._current_user_service.get_current_user()
            raise AlreadyAuthenticatedError()
        except AuthenticationError:
            pass

        raw_password = self._validate_password(request_data.password, request_data.repeat_password)
        hashed_password = await self._password_hasher.hash(raw_password.encode("utf-8"))

        user_role = await self._user_role_gateway.get_by_name(Role.PLAYER)

        bank_account = BankAccount(
            id=uuid6.uuid7(),
            balance=DEFAULT_USER_BANK_ACCOUNT_BALANCE
        )

        user_id=uuid6.uuid7()
        avatar_generator_url = await self._avatar_generator.generate_avatar(str(user_id))

        user = Users(
            id=user_id,
            hashed_password=hashed_password.decode(),
            email=request_data.email,
            username=request_data.username,
            role=user_role,
            bank_account_id=bank_account.id,
            avatar_url=avatar_generator_url
        )

        async with self._main_uow:
            try:
                await self._bank_account_gateway.add(bank_account)
                await self._user_gateway.add(user)
                await self._main_uow.commit()
            except UsernameAlreadyExistsError as e:
                raise e
            except EmailAlreadyExistsError as e:
                raise e
            except CommitError as err:
                raise ApplicationError from err

        logger.info("Sign up: done. Username: '%s'. Email: '%s'", user.email)
        return SignUpResponse(id=user.id)

    def _validate_password(self, password: str, repeat_password: str) -> str:

        if password != repeat_password:
            raise PasswordDoesntMatchError()

        return password