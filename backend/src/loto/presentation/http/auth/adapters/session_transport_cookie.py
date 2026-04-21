import logging

from starlette.requests import Request

from loto.infrastructure.auth.session.gateway.transport import AuthSessionTransport
from loto.infrastructure.auth.session.model import AuthSession
from loto.presentation.http.auth.constants import REQUEST_STATE_DELETE_SESSION_KEY, REQUEST_STATE_NEW_SESSION_ID_KEY, \
    REQUEST_STATE_COOKIE_PARAMS_KEY, SESSION_ID_DELIVERED_VIA_COOKIE, COOKIE_SESSION_ID_NAME, \
    SESSION_ID_MARKED_FOR_REMOVAL
from loto.presentation.http.auth.cookie_params import CookieParams

logger = logging.getLogger(__name__)

class CookieAuthSessionTransport(AuthSessionTransport):
    def __init__(
        self,
        request: Request,
        cookie_params: CookieParams,
    ) -> None:
        self._request = request

        self._cookie_params = cookie_params

    def deliver(self, auth_session: AuthSession) -> None:
        setattr(self._request.state, REQUEST_STATE_NEW_SESSION_ID_KEY, auth_session.id_)
        setattr(self._request.state, REQUEST_STATE_DELETE_SESSION_KEY, False)
        setattr(
            self._request.state,
            REQUEST_STATE_COOKIE_PARAMS_KEY,
            self._cookie_params,
        )

        logger.debug(
            "%s Session ID: %s",
            SESSION_ID_DELIVERED_VIA_COOKIE,
            auth_session.id_,
        )

    def extract_id(self) -> str | None:
        session_id = self._request.cookies.get(COOKIE_SESSION_ID_NAME)
        if not session_id:
            logger.debug("Session ID not found in cookie")
            return None
        return session_id

    def remove_current(self) -> None:
        setattr(self._request.state, REQUEST_STATE_DELETE_SESSION_KEY, True)
        setattr(self._request.state, REQUEST_STATE_NEW_SESSION_ID_KEY, False)

        logger.debug("%s", SESSION_ID_MARKED_FOR_REMOVAL)