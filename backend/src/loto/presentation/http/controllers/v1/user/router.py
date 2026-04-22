from fastapi import APIRouter

from loto.presentation.http.controllers.v1.user.bank_account.router import bank_account_router


def create_user_router() -> APIRouter:

    router = APIRouter(prefix="/user", tags=["User specific"])

    router.include_router(bank_account_router())

    return router