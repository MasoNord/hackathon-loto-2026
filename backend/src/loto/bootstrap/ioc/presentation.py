from dishka import Provider, from_context, Scope, provide
from starlette.requests import Request

from loto.bootstrap.config.security import CookiesConfig
from loto.infrastructure.auth.session.gateway.transport import AuthSessionTransport
from loto.presentation.http.auth.adapters.session_transport_cookie import CookieAuthSessionTransport
from loto.presentation.http.auth.cookie_params import CookieParams


class PresentationProvider(Provider):
    scope = Scope.REQUEST

    request = from_context(provides=Request)

    auth_session_transport = provide(CookieAuthSessionTransport, provides = AuthSessionTransport)

    @provide
    def provide_cookie_params(self, security: CookiesConfig) -> CookieParams:
        return CookieParams(secure=security.secure, samesite="none")
