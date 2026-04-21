import logging
from datetime import datetime
from uuid import UUID

from loto.application.common.uow import UoW
from loto.infrastructure.auth.session.gateway.auth_session import AuthSessionGateway
from loto.infrastructure.auth.session.gateway.transport import AuthSessionTransport
from loto.infrastructure.auth.session.id_generator import StrAuthSessionIdGenerator
from loto.infrastructure.auth.session.model import AuthSession
from loto.infrastructure.auth.session.timer import UtcAuthSessionTimer
from loto.infrastructure.exceptions.auth import AuthenticationError
from loto.infrastructure.exceptions.base import InfrastructureError

logger = logging.getLogger(__name__)

class AuthSessionService:

    def __init__(
            self,
            auth_session_gateway: AuthSessionGateway,
            auth_session_transport: AuthSessionTransport,
            auth_session_id_generator: StrAuthSessionIdGenerator,
            auth_session_timer: UtcAuthSessionTimer,
            uow: UoW,
    ):
        self._auth_session_gateway = auth_session_gateway
        self._auth_session_transport = auth_session_transport
        self._main_uow = uow
        self._auth_session_timer = auth_session_timer
        self._auth_session_id_generator = auth_session_id_generator

    async def issue_session(self, user_id: UUID, user_agent: str, ip_address: str) -> None:
        """:raises AuthenticationError:"""
        logger.debug("Issue auth session: started. User ID: '%s'.", user_id)

        auth_session_id: str = self._auth_session_id_generator.generate()
        expiration: datetime = self._auth_session_timer.auth_session_expiration
        auth_session = AuthSession(
            id_=auth_session_id,
            user_id=user_id,
            expiration=expiration,
            agent=user_agent,
            ip_address=ip_address
        )

        try:
            await self._auth_session_gateway.add(auth_session)
        except InfrastructureError as err:
            raise AuthenticationError from err

        self._auth_session_transport.deliver(auth_session)

        logger.debug(
            "Issue auth session: done. User ID: '%s', Auth session ID: '%s'.",
            user_id,
            auth_session.id_,
        )

    async def terminate_current_session(self) -> None:

        auth_session_id = self._auth_session_transport.extract_id()
        if auth_session_id is None:
            logger.warning(
                "Terminate current session failed: partially failed. "
                "Session ID can't be extracted from transport. "
                "Auth session can't be identified.",
            )
            return
        logger.debug(
            "Terminate current session: using ID from transport. "
            "Auth session ID: '%s'.",
            auth_session_id,
        )

        self._auth_session_transport.remove_current()

        await self._auth_session_gateway.delete(auth_session_id)
        logger.debug(
            "Terminate current session: done (transport cleared, storage deleted). "
            "Auth session ID: '%s'.",
            auth_session_id,
        )