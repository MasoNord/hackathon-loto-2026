from sqlalchemy import select

from loto.application.common.gateway.role_gateway import RoleGateway
from loto.domain.vo.role import Role
from loto.infrastructure.adapters.types import MainAsyncSession
from loto.infrastructure.persistence_sqla import Roles


class SARoleGateway(RoleGateway):
    def __init__(self, session: MainAsyncSession):
        self._session = session

    async def get_by_name(self, name: Role) -> Roles:
        stmt = select(Roles).filter_by(name=name)

        record = await self._session.execute(stmt)

        result = record.scalar_one()

        return result