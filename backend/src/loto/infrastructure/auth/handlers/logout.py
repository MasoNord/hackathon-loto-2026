import logging

from loto.application.common.services.current_user import CurrentUserService
from loto.infrastructure.auth.session.service import AuthSessionService

logger = logging.getLogger(__name__)

class Logout:

    def __init__(
        self,
        current_user_service: CurrentUserService,
        auth_session_service: AuthSessionService
    ) -> None:
        self._current_user_service = current_user_service
        self._auth_session_service = auth_session_service

    async def execute(self) -> None:

        logger.info("Log out: started for unknow user.")

        current_user = await self._current_user_service.get_current_user()

        logger.info("Log out: user identified. User ID: '%s'", current_user.id)

        await self._auth_session_service.terminate_current_session()

        logger.info("Log out: done. User ID: '%s'.", current_user.id)