import decimal
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.status import HTTP_200_OK

from loto.application.common.services.current_user import CurrentUserService
from loto.application.user.balance.withdraw import BankAccountWithDraw, BankAccountWithdrawRequest


class BankAccountWithdrawPydantic(BaseModel):
    amount: decimal.Decimal

def create_bank_account_withdraw_router() -> APIRouter:

    router = APIRouter()

    @router.put(
        "/{bank_account_id:uuid}",
        status_code=HTTP_200_OK
    )
    @inject
    async def bank_account_withdraw(
        interactor: FromDishka[BankAccountWithDraw],
        current_user_service: FromDishka[CurrentUserService],
        bank_account_id: UUID,
        request_withdraw: BankAccountWithdrawPydantic
    ):
        current_user = await current_user_service.get_current_user()

        bank_account_withdraw_request = BankAccountWithdrawRequest(
            money=request_withdraw.amount,
            bank_account_id=bank_account_id
        )

        return await interactor.execute(current_user, bank_account_withdraw_request)

    return router