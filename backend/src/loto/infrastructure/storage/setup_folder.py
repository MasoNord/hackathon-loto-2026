from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from loto.infrastructure.storage.constants import BASE_DIR

MEDIA_DIR = BASE_DIR / "media"

def set_media_folder(app: FastAPI):
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    
    app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")