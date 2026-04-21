from loto.domain.exceptions.base import DomainError


class UsernameAlreadyExistsError(DomainError):
    pass

class EmailAlreadyExistsError(DomainError):
    pass

class UserNotFoudByEmailError(DomainError):
    pass

class UserNotFoundById(DomainError):
    pass