from dishka import Provider, provide_all, provide, Scope

from loto.application.common.gateway.bank_account_gateway import BankAccountGateway
from loto.application.common.gateway.identity_provider import IdentityProvider
from loto.application.common.gateway.role_gateway import RoleGateway
from loto.application.common.gateway.room_gateway import RoomGateway
from loto.application.common.gateway.room_participants_gateway import RoomParticipantsGateway
from loto.application.common.gateway.user_gateway import UserGateway
from loto.application.common.gateway.withdraw_balance_history_gateway import WithdrawBalanceHistoryGateway
from loto.application.common.services.avatar_generator import AvatarGenerator
from loto.application.common.services.current_user import CurrentUserService
from loto.application.common.uow import UoW
from loto.application.room.create import CreateRoom
from loto.application.room.read import ReadRooms, ReadRoomByID
from loto.application.room_participants.join import JoinRoom
from loto.application.user.balance.withdraw import BankAccountWithDraw
from loto.infrastructure.auth.idp.identity_provider import FastAPIIdentityProvider
from loto.infrastructure.persistence_sqla.gateway.bank_account_gateway import SABankAccountGateway
from loto.infrastructure.persistence_sqla.gateway.role_gateway import SARoleGateway
from loto.infrastructure.persistence_sqla.gateway.room_gateway import SARoomGateway
from loto.infrastructure.persistence_sqla.gateway.room_participant_gateway import SARoomParticipantGateway
from loto.infrastructure.persistence_sqla.gateway.user_gateway import SAUserGateway
from loto.infrastructure.persistence_sqla.gateway.withdraw_balance_history_gateway import \
    SAWithdrawBalanceHistoryGateway
from loto.infrastructure.persistence_sqla.uow import BaseSQLAlchemyUoW


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    services = provide_all(CurrentUserService, AvatarGenerator)

    uow = provide(BaseSQLAlchemyUoW, provides=UoW)

    identity_provider = provide(FastAPIIdentityProvider, provides=IdentityProvider)

    user_gateway = provide(SAUserGateway, provides=UserGateway)

    user_role_gateway = provide(SARoleGateway, provides=RoleGateway)

    bank_account_gateway = provide(SABankAccountGateway, provides=BankAccountGateway)

    room_gateway = provide(SARoomGateway, provides=RoomGateway)

    bank_account_withdraw_history_gateway = provide(SAWithdrawBalanceHistoryGateway, provides=WithdrawBalanceHistoryGateway)

    room_participant_gateway = provide(SARoomParticipantGateway, provides=RoomParticipantsGateway)

    use_cases = provide_all(
        CreateRoom,
        ReadRooms,
        BankAccountWithDraw,
        ReadRoomByID,
        JoinRoom
    )