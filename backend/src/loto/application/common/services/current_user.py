import logging

from loto.application.common.gateway.identity_provider import IdentityProvider
from loto.application.common.gateway.user_gateway import UserGateway
from loto.infrastructure.persistence_sqla import Users

logger = logging.getLogger(__name__)

class CurrentUserService:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        user_gateway: UserGateway,
    ) -> None:
        self._identity_provider = identity_provider
        self._user_gateway = user_gateway

    async def get_current_user(self) -> Users:
        """
        :raises AuthenticationError:
        :raises DataMapperError:
        :raises AuthorizationError:
        """
        current_user_id = await self._identity_provider.get_current_user_id()

        logger.info("Current user profile id: %s", current_user_id)

        user: Users | None = await self._user_gateway.get_by_id(
            current_user_id
        )

        return user