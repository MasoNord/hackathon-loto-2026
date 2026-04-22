from loto.application.exceptions.base import ApplicationError
from loto.application.exceptions.room import RoomNotFoundError
from loto.application.exceptions.room_participants import NotEnoughMoneyError
from loto.domain.exceptions.base import DomainError
from loto.domain.exceptions.user import UserNotFoudByEmailError, UsernameAlreadyExistsError, EmailAlreadyExistsError
from loto.infrastructure.exceptions.auth import AuthenticationError, PasswordDoesntMatchError, AlreadyAuthenticatedError
from loto.infrastructure.exceptions.base import InfrastructureError

ERROR_HTTP_CODE = {
    ApplicationError: 500,
    InfrastructureError: 500,
    DomainError: 500,

    NotEnoughMoneyError: 400,

    UserNotFoudByEmailError: 404,
    RoomNotFoundError: 404,

    AuthenticationError: 401,
    PasswordDoesntMatchError: 401,

    UsernameAlreadyExistsError: 409,
    EmailAlreadyExistsError: 409,
    AlreadyAuthenticatedError: 409,
}

ERROR_MESSAGE = {
    NotEnoughMoneyError: "Not enough money error",
    RoomNotFoundError: "Room not found error",
    ApplicationError: "Unhanded application error",
    InfrastructureError: "Unhanded infrastructure error",
    DomainError: "Unhanded application error",
    UserNotFoudByEmailError: "User email not found",
    PasswordDoesntMatchError: "Supplied wrong user password",
    AuthenticationError: "Authentication error",
    UsernameAlreadyExistsError: "Username already exist error",
    EmailAlreadyExistsError: "Email already exists error",
    AlreadyAuthenticatedError: "User already authenticated error",
}

ERROR_CODE = {
    ApplicationError: "UNHANDLED",
    NotEnoughMoneyError: "NOT_ENOUGH_MONEY",
    RoomNotFoundError: "ROOM_NOT_FOUND",
    InfrastructureError: "UNHANDLED",
    DomainError: "UNHANDLED",
    PasswordDoesntMatchError: "INVALID_USER_PASSWORD",
    AuthenticationError: "AUTHENTICATION_ERROR",
    UsernameAlreadyExistsError: "USERNAME_ALREADY_EXIST",
    EmailAlreadyExistsError: "EMAIL_ALREADY_EXISTS",
    UserNotFoudByEmailError: "USER_EMAIL_NOT_FOUND",
    AlreadyAuthenticatedError: "USER_ALREADY_AUTHENTICATED",
}