from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.requests import Request
from starlette.status import HTTP_204_NO_CONTENT

from loto.infrastructure.auth.handlers.login import LogInRequest, Login


class LogInRequestPydantic(BaseModel):
    username: str
    password: str

def create_login_router() -> APIRouter:
    router = APIRouter()

    @router.post(
        "/login",
        status_code=HTTP_204_NO_CONTENT
    )
    @inject
    async def login (
        request_data: LogInRequestPydantic,
        interactor: FromDishka[Login],
        request: Request
    ) -> None:
        await interactor.execute(LogInRequest(username=request_data.username, password=request_data.password), request)
    return router
