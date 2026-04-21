from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class AuthSession:
    id_: str
    user_id: UUID
    agent: str
    ip_address: str
    expiration: datetime