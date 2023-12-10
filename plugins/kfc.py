# coding = utf-8
import sys
import requests

sys.path.append('..')
import logging


from peanut_bot.manager import plugin
from peanut_bot.utils import GroupAtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def ping(api:QOpenApi,event: GroupAtMessageEvent):
    if not isinstance(event,GroupAtMessageEvent):
        return
    if event.content.startswith(' kfc') or event.content.startswith('kfc'):
        url = "https://api.jixs.cc/api/wenan-fkxqs/index.php?type=json"
        message=requests.get(url).json()[0]['kfc']
        await api.send(event.group_openid,
                       message=f'{message}')

