

from fastapi import APIRouter

from loto.presentation.http.controllers.v1.account.router import create_account_router
from loto.presentation.http.controllers.v1.general.router import create_general_router


def create_api_v1_router() -> APIRouter:
    router = APIRouter(prefix="/api/v1")

    router.include_router(create_general_router())
    router.include_router(create_account_router())

    return router