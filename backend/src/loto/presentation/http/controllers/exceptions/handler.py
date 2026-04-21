from fastapi import Request
from starlette.responses import Response
import json

from loto.application.exceptions.base import ApplicationError
from loto.domain.exceptions.base import DomainError
from loto.infrastructure.exceptions.base import InfrastructureError
from loto.presentation.http.controllers.exceptions.constants import ERROR_MESSAGE, ERROR_HTTP_CODE, ERROR_CODE


async def app_error_handler(request: Request, e: ApplicationError) -> Response:
    content = {
        "description": ERROR_MESSAGE[type(e)],
        "unique_code": ERROR_CODE[type(e)],
    }

    return Response(
        content=json.dumps(content),
        status_code=ERROR_HTTP_CODE[type(e)],
        media_type="application/json"
    )

async def infrastructure_error_handler(request: Request, e: InfrastructureError) -> Response:
    content = {
        "description": ERROR_MESSAGE[type(e)],
        "unique_code": ERROR_CODE[type(e)],
    }

    return Response(
        content=json.dumps(content),
        status_code=ERROR_HTTP_CODE[type(e)],
        media_type="application/json"
    )

async def domain_error_handler(request: Request, e: DomainError) -> Response:
    content = {
        "description": ERROR_MESSAGE[type(e)],
        "unique_code": ERROR_CODE[type(e)],
    }

    return Response(
        content=json.dumps(content),
        status_code=ERROR_HTTP_CODE[type(e)],
        media_type="application/json"
    )