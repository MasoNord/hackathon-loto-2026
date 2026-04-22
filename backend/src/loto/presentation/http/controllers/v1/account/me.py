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
    username: str
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
            role=me.role.name,
            username=me.username,
            bank_account=me.bank_account
        )

    return router