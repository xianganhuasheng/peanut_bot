'''base on satoriv1'''

from dataclasses import dataclass
from typing import Optional


from ..models.channel import Channel
from ..models.guild import Guild
from ..models.user import User
from ..models.guild_member import GuildMember
from ..models.guild_role import GuildRole
from ..models.interaction import Argv, Button
from ..models.login import Login
from ..models.message import Message

    
@dataclass
class SatoriEvent():
    id: int
    type: str
    platform: str
    self_id: str
    timestamp: int
    argv: Optional[Argv]  = None
    button: Optional[Button]  = None
    channel: Optional[Channel]  = None
    guild: Optional[Guild]  = None
    login: Optional[Login]  = None
    member: Optional[GuildMember]  = None
    message: Optional[Message]  = None
    operator: Optional[User]  = None
    role: Optional[GuildRole]  = None
    user: Optional[User]  = None



