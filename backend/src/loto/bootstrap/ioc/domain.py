from dishka import Provider, provide, Scope

from loto.domain.gateway.password_hasher import PasswordHasher
from loto.domain.services.user_service import UserService
from loto.infrastructure.adapters.password_hasher import ArgonPasswordHasher


class DomainProvider(Provider):
    scope = Scope.APP

    user_service = provide(UserService)

    password_hasher = provide(ArgonPasswordHasher, provides=PasswordHasher)
