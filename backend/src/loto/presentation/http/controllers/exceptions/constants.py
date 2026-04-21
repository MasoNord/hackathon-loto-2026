from loto.application.exceptions.base import ApplicationError
from loto.infrastructure.exceptions.base import InfrastructureError
from loto.domain.exceptions.base import DomainError

ERROR_HTTP_CODE = {
    ApplicationError: 500,
    InfrastructureError: 500,
    DomainError: 500,

}

ERROR_MESSAGE = {
    ApplicationError: "Unhanded application error",
    InfrastructureError: "Unhanded infrastructure error",
    DomainError: "Unhanded application error",
}

ERROR_CODE = {
    ApplicationError: "UNHANDLED",
    InfrastructureError: "UNHANDLED",
    DomainError: "UNHANDLED",
}