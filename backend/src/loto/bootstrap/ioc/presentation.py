from dishka import Provider, from_context, Scope, provide
from starlette.requests import Request

from loto.bootstrap.config.security import CookiesConfig
from loto.infrastructure.auth.session.gateway.transport import AuthSessionTransport
from loto.presentation.http.auth.adapters.session_transport_cookie import CookieAuthSessionTransport
from loto.presentation.http.auth.cookie_params import CookieParams
from loto.presentation.websockets.adapters.fastapi_connection_manager import FastApiConnectionManager
from loto.presentation.websockets.connections.gateway.connection_manager import ConnectionManager


class PresentationProvider(Provider):
    scope = Scope.REQUEST

    request = from_context(provides=Request)

    auth_session_transport = provide(CookieAuthSessionTransport, provides = AuthSessionTransport)

    @provide
    def provide_cookie_params(self, security: CookiesConfig) -> CookieParams:
        return CookieParams(secure=security.secure, samesite="none")


class WebSocketProvider(Provider):
    scope = Scope.SESSION

    connection_manager = provide(FastApiConnectionManager, provides=ConnectionManager)

def presentation_providers() -> tuple[Provider, ...]:
    return (
        PresentationProvider(),
        WebSocketProvider()
    )
