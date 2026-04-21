from dishka import Provider, provide, Scope

from loto.domain.gateway.password_hasher import PasswordHasher
from loto.infrastructure.adapters.password_hasher import ArgonPasswordHasher


class DomainProvider(Provider):
    scope = Scope.APP

    password_hasher = provide(ArgonPasswordHasher, provides=PasswordHasher)
