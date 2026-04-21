from fastapi import APIRouter

from loto.presentation.http.controllers.v1.account.signup import create_sign_up_router


def create_account_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["Auth specific"])

    router.include_router(create_sign_up_router())
    # router.include_router(create_login_router())
    # router.include_router(create_logout_router())
    # router.include_router(create_get_me_router())

    return router