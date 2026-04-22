import argon2.exceptions

from loto.domain.gateway.password_hasher import PasswordHasher
from loto.infrastructure.persistence_sqla import Users


class UserService:

    def __init__(self, password_hasher: PasswordHasher):
        self._password_hasher=password_hasher

    async def verify_password(self, user: Users, password: bytes) -> bool:
        try:
            await self._password_hasher.verify(password, user.hashed_password.encode())
        except argon2.exceptions.VerifyMismatchError:
            return False

        return True