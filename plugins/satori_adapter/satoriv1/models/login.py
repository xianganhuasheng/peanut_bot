from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from .user import User


class Status(Enum):
    OFFLINE = 0
    ONLINE = 1
    CONNECT = 2
    DISCONNECT = 3
    RECONNECT = 4


@dataclass
class Login:
    status: Status
    features: List[str]
    proxy_urls: List[str]
    user: Optional[User] = None
    self_id: Optional[str] = None
    platform: Optional[str] = None