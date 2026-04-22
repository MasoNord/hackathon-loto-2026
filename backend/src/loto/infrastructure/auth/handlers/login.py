import logging
from dataclasses import dataclass

from starlette.requests import Request

from loto.application.common.gateway.user_gateway import UserGateway
from loto.application.common.services.current_user import CurrentUserService
from loto.domain.exceptions.user import UserNotFoudByEmailError
from loto.domain.services.user_service import UserService
from loto.infrastructure.auth.session.service import AuthSessionService
from loto.infrastructure.exceptions.auth import AlreadyAuthenticatedError, AuthenticationError, PasswordDoesntMatchError

logger = logging.getLogger(__name__)

@dataclass(frozen=True, slots=True, kw_only=True)
class LogInRequest:
    email: str
    password: str

class Login:
    def __init__(
        self,
        user_gateway: UserGateway,
        current_user_service: CurrentUserService,
        auth_session_service: AuthSessionService,
        user_service: UserService
    ):
        self._user_gateway=user_gateway
        self._current_user_service=current_user_service
        self._auth_session_service=auth_session_service
        self._user_service=user_service

    async def execute(self, request_data: LogInRequest, request: Request):

        logger.info("Log in: started. Email: '%s'", request_data.email)

        try:
            await self._current_user_service.get_current_user()
            raise AlreadyAuthenticatedError
        except AuthenticationError:
            pass

        user = await self._user_gateway.get_by_email(request_data.email)

        if not user:
            raise UserNotFoudByEmailError(request_data.email)

        if not await self._user_service.verify_password(user, request_data.password.encode()):
            raise PasswordDoesntMatchError

        await self._auth_session_service.issue_session(user.id, request.headers.get("user-agent"), request.client.host)

        logger.info(
            "Log in: done. User, ID: '%s', username '%s'",
            user.id
        )

