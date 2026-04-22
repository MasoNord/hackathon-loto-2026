import logging
from uuid import UUID

from loto.application.common.gateway.identity_provider import IdentityProvider
from loto.infrastructure.auth.session.gateway.auth_session import AuthSessionGateway
from loto.infrastructure.auth.session.gateway.transport import AuthSessionTransport
from loto.infrastructure.auth.session.id_generator import StrAuthSessionIdGenerator
from loto.infrastructure.auth.session.model import AuthSession
from loto.infrastructure.auth.session.timer import UtcAuthSessionTimer
from loto.infrastructure.exceptions.auth import AuthenticationError
from loto.infrastructure.exceptions.base import InfrastructureError

logger = logging.getLogger(__name__)


class FastAPIIdentityProvider(IdentityProvider):

    def __init__(
        self,
        auth_session_transport: AuthSessionTransport,
        auth_session_timer: UtcAuthSessionTimer,
        auth_session_id_generator: StrAuthSessionIdGenerator,
        auth_session_gateway: AuthSessionGateway,

    ):
        self._auth_session_transport=auth_session_transport
        self._auth_session_timer = auth_session_timer
        self._auth_session_id_generator = auth_session_id_generator
        self._auth_session_gateway = auth_session_gateway

    async def get_current_user_id(self) -> UUID:
        """:raises AuthenticationError:"""
        logger.debug("Get authenticated user ID: started.")

        raw_auth_session = await self._get_current_auth_session()
        valid_auth_session = await self._validate_and_extend_session(raw_auth_session)

        logger.debug (
            "Get authenticated user ID: done. Auth session ID: '%s'. User ID: '%s'.",
            valid_auth_session.id_,
            valid_auth_session.user_id,
        )
        return valid_auth_session.user_id


    async def _get_current_auth_session(self) -> AuthSession:
        """:raises AuthenticationError:"""
        logger.debug("Get current auth session: started. Auth session ID: unknown.")

        auth_session_id: str | None = self._auth_session_transport.extract_id()
        if auth_session_id is None:
            self._auth_session_transport.remove_current()
            raise AuthenticationError

        logger.debug(
            "Get current auth session: reading from storage. Auth session ID: '%s'.",
            auth_session_id,
        )

        try:
            auth_session: (AuthSession | None) = await self._auth_session_gateway.get_by_id(auth_session_id)

        except InfrastructureError:
            self._auth_session_transport.remove_current()
            raise AuthenticationError

        if auth_session is None:
            self._auth_session_transport.remove_current()
            raise AuthenticationError

        logger.debug(
            "Get current auth session: done. Auth session ID: '%s'.", auth_session.id_
        )
        return auth_session

    async def _validate_and_extend_session(
            self,
            auth_session: AuthSession,
    ) -> AuthSession:
        """:raises AuthenticationError:"""
        logger.debug(
            "Validate and extend auth session: started. Auth session ID: '%s'.",
            auth_session.id_,
        )

        now = self._auth_session_timer.current_time
        if auth_session.expiration <= now:
            raise AuthenticationError

        if (
                auth_session.expiration - now
                > self._auth_session_timer.refresh_trigger_interval
        ):
            logger.debug(
                "Validate and extend auth session: validated without extension. "
                "Auth session ID: '%s'.",
                auth_session.id_,
            )
            return auth_session

        original_expiration = auth_session.expiration
        auth_session.expiration = self._auth_session_timer.auth_session_expiration

        try:
            await self._auth_session_gateway.update(auth_session)
        except InfrastructureError:
            auth_session.expiration = original_expiration
            return auth_session

        self._auth_session_transport.deliver(auth_session)

        logger.debug(
            "Validate and extend auth session: done. "
            "Auth session ID: '%s'. New expiration: '%s'.",
            auth_session.id_,
            auth_session.expiration.isoformat(),
        )
        return auth_session