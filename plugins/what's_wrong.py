import logging
import aiofiles
import json

from peanut_bot.manager import load_config, plugin
from peanut_bot.driver.http import QOpenApi
from peanut_bot.utils.event import AtMessageEvent


@plugin
async def qerror_tips(api: QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    if event.content.startswith('/我错哪了'):
        code = event.content[6:]
        async with aiofiles.open("data/qerror.json",'r',encoding="utf-8") as errors:
            if wrong := json.loads(await errors.read()).get(code):
                await api.send(event,wrong)
            else:
                await api.send(event,"没有查询到相关信息")