from fastapi import APIRouter

from loto.presentation.http.controllers.v1.user.bank_account.withdraw import create_bank_account_withdraw_router


def bank_account_router() -> APIRouter:

    router = APIRouter(prefix="/bank-account")

    router.include_router(create_bank_account_withdraw_router())

    return router