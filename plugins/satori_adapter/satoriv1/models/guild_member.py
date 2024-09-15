from dataclasses import dataclass
from typing import Optional


from .user import User


@dataclass
class GuildMember:
    user: Optional[User] = None
    nick: Optional[str] = None
    avatar: Optional[str] = None
    joined_at: Optional[int] = None
    

