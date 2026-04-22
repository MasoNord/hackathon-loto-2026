from fastapi import APIRouter

from loto.presentation.http.controllers.v1.account.login import create_login_router
from loto.presentation.http.controllers.v1.account.logout import create_logout_router
from loto.presentation.http.controllers.v1.account.me import create_get_me_router
from loto.presentation.http.controllers.v1.account.signup import create_sign_up_router


def create_account_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["Auth specific"])

    router.include_router(create_sign_up_router())
    router.include_router(create_login_router())
    router.include_router(create_logout_router())
    router.include_router(create_get_me_router())

    return router