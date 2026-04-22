from pathlib import Path

import aiofiles
import aiofiles.os

from loto.infrastructure.storage.gateway.file_manager import FileManager


class LocalStorageFileManager(FileManager):

    async def upload(self, filepath: Path, content: bytes) -> None:
        async with aiofiles.open(filepath, "wb") as f:
            await f.write(content)


    async def delete(self, filepath: str) -> None:
        path = Path(filepath)

        if await aiofiles.os.path.exists(path):
            await aiofiles.os.remove(path)