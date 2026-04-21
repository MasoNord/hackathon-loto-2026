import logging
from http.cookies import SimpleCookie
from typing import Literal
from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from loto.presentation.http.auth.constants import REQUEST_STATE_NEW_SESSION_ID_KEY, REQUEST_STATE_COOKIE_PARAMS_KEY, \
    COOKIE_SESSION_ID_NAME, REQUEST_STATE_DELETE_SESSION_KEY
from loto.presentation.http.auth.cookie_params import CookieParams

logger = logging.getLogger(__name__)

class ASGISessionMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        logger.debug("Initialize ASGI session middleware")
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope)

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                self._set_cookie(request, headers)
                self._delete_cookie(request, headers)
            await send(message)

        return await self.app(scope, receive, send_wrapper)

    def _set_cookie(self, request: Request, headers: MutableHeaders) -> None:
        new_session_id: str | None = getattr(
            request.state,
            REQUEST_STATE_NEW_SESSION_ID_KEY,
            None,
        )
        if new_session_id is None:
            return

        cookie_params: CookieParams = getattr(
            request.state,
            REQUEST_STATE_COOKIE_PARAMS_KEY,
            CookieParams(secure=False),
        )
        if cookie_params is None:
            return

        cookie_header = self._make_cookie_header(
            name=COOKIE_SESSION_ID_NAME,
            value=new_session_id,
            is_secure=cookie_params.secure,
            samesite=cookie_params.samesite,
        )
        headers.append("Set-Cookie", cookie_header)
        logger.debug("Cookie with session ID '%s' was set.", new_session_id)

    def _delete_cookie(self, request: Request, headers: MutableHeaders) -> None:
        if not getattr(request.state, REQUEST_STATE_DELETE_SESSION_KEY, False):
            logger.debug("Request state delete session key is false")
            return

        cookie_params = getattr(request.state, REQUEST_STATE_COOKIE_PARAMS_KEY, CookieParams(secure=False))

        cookie_header = self._make_cookie_header(
            name=COOKIE_SESSION_ID_NAME,
            value="",
            max_age=0,
            is_secure=cookie_params.secure,
            samesite=cookie_params.samesite,
        )
        headers.append("Set-Cookie", cookie_header)
        logger.debug("Cookie was deleted.")

    def _make_cookie_header(
        self,
        *,
        name: str,
        value: str,
        is_secure: bool = True,
        samesite: Literal["strict"] | None = None,
        max_age: int | None = None,
    ) -> str:
        cookie = SimpleCookie()
        cookie[name] = value
        cookie[name]["path"] = "/"
        cookie[name]["httponly"] = True
        cookie[name]["secure"] = is_secure

        if samesite:
            cookie[name]["samesite"] = samesite

        if max_age is not None:
            cookie[name]["max-age"] = max_age

        return cookie.output(header="").strip()