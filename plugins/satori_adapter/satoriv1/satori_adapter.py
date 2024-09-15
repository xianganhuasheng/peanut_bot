from .models.channel import Channel
from .models.user import User
from .models.guild import Guild
from .models.guild_member import GuildMember
from .models.guild_role import GuildRole
from .models.message import Message

from .events.satoriv1_events import SatoriEvent

from peanut_bot.utils import Event, GroupAtMessageEvent


def parser(event: Event) -> SatoriEvent:
    if isinstance(event,GroupAtMessageEvent):
        return None
    


    
# def deparser(event: SatoriEvent):
#     if isinstance(event, SatoriEvent):
#         return GroupAtMessageEvent(event.raw_data["raw_data"])