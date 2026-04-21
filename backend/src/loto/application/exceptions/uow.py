from loto.application.exceptions.base import ApplicationError


class DeletionError(ApplicationError):
    pass

class FlushError(ApplicationError):
    pass

class AddInstanceError(ApplicationError):
    pass

class CommitError(ApplicationError):
    pass

class RollbackError(ApplicationError):
    pass