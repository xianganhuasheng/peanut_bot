# coding = utf-8
import sys
import requests

sys.path.append('..')
import logging


from peanut_bot.manager import plugin
from peanut_bot.utils import GroupAtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def poem(api:QOpenApi,event: GroupAtMessageEvent):
    if not isinstance(event,GroupAtMessageEvent):
        return
    if event.content in ["/poem",'/诗',' /poem',' /诗']:
        url = "http://www.wudada.online/Api/ScSj"
        message = "\n"+"。\n".join(requests.get(url).json()["data"].split("。"))
        await api.send(event,
                       message=f'{message}')

