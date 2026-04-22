from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.status import HTTP_200_OK

from loto.application.common.services.current_user import CurrentUserService
from loto.infrastructure.auth.handlers.me import Me, BankAccountRead


class UserReadMePydantic(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    middle_name: str
    email: str
    role: str
    bank_account: BankAccountRead

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

def create_get_me_router() -> APIRouter:

    router = APIRouter()

    @router.get(
        "/me",
        status_code=HTTP_200_OK,
    )
    @inject
    async def get_me (
        interactor: FromDishka[Me],
        current_user_service: FromDishka[CurrentUserService],
    ) -> UserReadMePydantic:

        current_user = await current_user_service.get_current_user()

        me = await interactor.execute(current_user)


        return UserReadMePydantic(
            id=me.id,
            first_name=me.first_name,
            last_name=me.last_name,
            middle_name=me.middle_name,
            email=me.email,
            role=me.role.name,
            bank_account=me.bank_account
        )

    return router