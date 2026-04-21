from abc import abstractmethod
from typing import Protocol

from loto.domain.vo.role import Role
from loto.infrastructure.persistence_sqla import Roles


class RoleGateway(Protocol):

    @abstractmethod
    async def get_by_name(self, name: Role) -> Roles:
        raise NotImplementedError