# coding = utf-8
import sys
import requests

sys.path.append('..')
import logging


from peanut_bot.manager import plugin
from peanut_bot.utils import AtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def fabing(api:QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    if event.content.startswith('/fb'):
        name=event.content.split(" ")[-1]
        if name == "/fb":
            await api.send(event,
                           message=f'命令错误！')
        else:
            url = "https://api.lolimi.cn/API/fabing/fb.php"
            params = {"name": {name}}
            data = requests.get(url, params=params).json()["data"]
            await api.send(event,
                           message=f'\n{data}')

