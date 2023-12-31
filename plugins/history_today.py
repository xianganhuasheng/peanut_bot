# coding = utf-8
import sys
import requests

sys.path.append('..')
import logging


from peanut_bot.manager import plugin
from peanut_bot.utils import AtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def history_today(api:QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    if event.content in ["/history",'/today']:
        url = "https://zj.v.api.aa1.cn/api/bk/"
        params = {"type": "json"}
        data = requests.get(url, params=params).json()
        message, n = f"\n历史上的今天:{data['day']}", 0
        for i in data["content"]:
            n = n + 1
            message = message + f"\n{n}.{i}"
        await api.send(event,
                       message=f'{message}')

