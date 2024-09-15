from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: str
    name: Optional[str] = None
    nick: Optional[str] = None
    avatar: Optional[str] = None
    is_bot: Optional[bool] = None