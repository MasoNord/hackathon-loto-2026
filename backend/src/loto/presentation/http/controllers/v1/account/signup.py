from inspect import getdoc

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED

from loto.infrastructure.auth.handlers.signup import SignUpResponse, SignUp, SignUpRequest


class SingUpRequestPydantic(BaseModel):
    password: str
    repeat_password: str
    username: str
    email: str

def create_sign_up_router() -> APIRouter:
    router = APIRouter()

    @router.post(
        "/signup",
        description=getdoc(SignUp),
        status_code=HTTP_201_CREATED,
    )
    @inject
    async def sign_up(
        request_data_pydantic: SingUpRequestPydantic,
        interactor: FromDishka[SignUp]
    ) -> SignUpResponse:
        request_data = SignUpRequest(
            password=request_data_pydantic.password,
            repeat_password=request_data_pydantic.repeat_password,
            email=request_data_pydantic.email,
            username=request_data_pydantic.username
        )

        return await interactor.execute(request_data)
    return router