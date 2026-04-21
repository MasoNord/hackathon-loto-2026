from typing import Any, Sequence
from sqlalchemy.exc import SQLAlchemyError

from loto.application.common.uow import UoW
from loto.application.exceptions.uow import FlushError, CommitError, RollbackError
from loto.infrastructure.adapters.types import MainAsyncSession

class BaseSQLAlchemyUoW(UoW):

    def __init__(self, session: MainAsyncSession):
        self._session = session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self._session.rollback()

    async def flush(self, objects: Sequence[Any] | None = None) -> None:
        try:
            await self._session.flush(objects)
        except SQLAlchemyError as err:
            await self._session.rollback()
            raise FlushError from err

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError from err
