from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserSession:
    user_id: UUID
    session_id: str
    expire_at: datetime
    agent: str
    ip_address: str