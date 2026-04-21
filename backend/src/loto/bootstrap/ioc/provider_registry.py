from typing import Iterable

from dishka import Provider

from loto.bootstrap.ioc.application import ApplicationProvider
from loto.bootstrap.ioc.domain import DomainProvider
from loto.bootstrap.ioc.infrastructure import infrastructure_providers
from loto.bootstrap.ioc.presentation import PresentationProvider
from loto.bootstrap.ioc.settings import SettingsProvider


def get_providers() -> Iterable[Provider]:
    return (
        SettingsProvider(),
        PresentationProvider(),
        *infrastructure_providers(),
        ApplicationProvider(),
        DomainProvider()
    )