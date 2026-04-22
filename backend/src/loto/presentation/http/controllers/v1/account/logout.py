from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_204_NO_CONTENT

from loto.infrastructure.auth.handlers.logout import Logout


def create_logout_router() -> APIRouter:
    router = APIRouter()

    @router.post(
        "/logout",
        status_code=HTTP_204_NO_CONTENT
    )
    @inject
    async def logout(
        interactor: FromDishka[Logout]
    ) -> None:
        await interactor.execute()

    return router