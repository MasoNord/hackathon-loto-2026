from abc import abstractmethod
from pathlib import Path
from typing import Protocol


class FileManager(Protocol):

    @abstractmethod
    async def upload(self, filepath: Path, content: bytes) -> None:
        raise NotImplementedError


    @abstractmethod
    async def delete(self, filepath: str) -> None:
        raise NotImplementedError