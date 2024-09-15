from .onebotv11_model import Ob11Event, Ob11GroupMessageEvent

from peanut_bot.utils import Event, GroupAtMessageEvent


def parser(event: Event) -> Ob11Event:
    if isinstance(event,GroupAtMessageEvent):
        return Ob11GroupMessageEvent(
            {
                "time":event.time,
                "self_id":event.event_id,
                "post_type":"message",
                "message_type": "group",
                "message_id":event.message_id,
                "user_id": event.author["id"],
                "message": event.content,
                "raw_message": event.data["content"],
                "font": None,
                "sender": event.author,
                "group_id": event.group_id,
                "anonymous": None,
                "sub_type": "normal",
                "raw_data": event.data,
            }
        )
    
def deparser(event: Ob11Event):
    if isinstance(event, Ob11GroupMessageEvent):
        return GroupAtMessageEvent(event.raw_data["raw_data"])