from abc import abstractmethod
from typing import Protocol, List, Any


class UoW(Protocol):
    async def __aenter__(self) -> "UoW":
        ...

    async def __aexit__(self, exc_type, exc, tb) -> None:
        ...

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def flush(self, objects: List[Any] | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError