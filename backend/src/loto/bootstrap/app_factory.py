from contextlib import asynccontextmanager
from typing import AsyncIterator

from dishka import AsyncContainer, make_async_container, Provider
from fastapi import FastAPI
from loto.application.exceptions.base import ApplicationError
from loto.bootstrap.ioc.provider_registry import get_providers
from loto.domain.exceptions.base import DomainError
from loto.infrastructure.exceptions.base import InfrastructureError
from loto.infrastructure.storage.setup_folder import set_media_folder
from loto.presentation.http.auth.asgi_middleware import ASGISessionMiddleware
from loto.presentation.http.auth.setup_cors import setup_cors
from loto.presentation.http.controllers.exceptions.handler import app_error_handler, infrastructure_error_handler, \
    domain_error_handler
from loto.presentation.http.controllers.root_router import create_root_router


def create_ioc_container(
    *di_providers: Provider,
) -> AsyncContainer:
    return make_async_container(
        *get_providers(),
        *di_providers
    )

def create_web_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan
    )

    app.include_router(create_root_router())

    app.add_exception_handler(ApplicationError, app_error_handler)
    app.add_exception_handler(InfrastructureError, infrastructure_error_handler)
    app.add_exception_handler(DomainError, domain_error_handler)

    setup_cors(app)

    app.add_middleware(ASGISessionMiddleware)

    set_media_folder(app)

    return app

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    container = app.state.dishka_container
    try:
        yield
    finally:
        await container.close()