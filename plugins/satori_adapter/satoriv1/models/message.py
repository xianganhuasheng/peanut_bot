from dataclasses import dataclass
from typing import Optional


from .channel import Channel
from .guild import Guild
from .guild_member import GuildMember
from .user import User


@dataclass
class Message:
    id: str
    content: str
    channel: Optional[Channel] = None
    guild: Optional[Guild] = None
    member: Optional[GuildMember] = None
    user: Optional[User] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None