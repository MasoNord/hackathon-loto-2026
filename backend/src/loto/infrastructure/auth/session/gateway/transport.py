from abc import abstractmethod
from typing import Protocol

from loto.infrastructure.auth.session.model import AuthSession


class AuthSessionTransport(Protocol):
    @abstractmethod
    def deliver(self, auth_session: AuthSession) -> None:
        raise NotImplementedError

    @abstractmethod
    def extract_id(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def remove_current(self) -> None:
        raise NotImplementedError
