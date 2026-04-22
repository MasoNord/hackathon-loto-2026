from pathlib import Path

import pydenticon


from loto.infrastructure.storage.gateway.file_manager import FileManager
from loto.infrastructure.storage.setup_folder import MEDIA_DIR

AVATAR_DIR = MEDIA_DIR / "avatars"

generator = pydenticon.Generator(
    10, 10,
    foreground=[
        "rgb(45,79,255)",
        "rgb(254,180,44)",
        "rgb(226,121,234)",
        "rgb(30,179,253)",
        "rgb(232,77,65)",
        "rgb(49,203,115)",
        "rgb(141,69,170)"
    ],
    background="rgb(224,224,224)"
)


class AvatarGenerator:

    def __init__(self, file_manager: FileManager):
        self._file_manager=file_manager

    async def generate_avatar(self, user_id: str) -> str:
        AVATAR_DIR.mkdir(parents=True, exist_ok=True)

        file_path = AVATAR_DIR / f"{user_id}.png"

        png = generator.generate(user_id, 300, 300)


        await self._file_manager.upload(file_path, png)


        parts = file_path.parts

        media_index = parts.index("media")

        relative = Path(*parts[media_index:])

        return str(relative)
