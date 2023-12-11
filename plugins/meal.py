import logging
import random
import requests

from peanut_bot.manager import plugin
from peanut_bot.utils import GroupAtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

# print("loaded")


@plugin
async def meal(api:QOpenApi,event: GroupAtMessageEvent):
    if not isinstance(event,GroupAtMessageEvent):
        return
    if event.content.startswith('/meal') or event.content.startswith(' /meal'):
        url = "https://zj.v.api.aa1.cn/api/eats/"
        data = requests.get(url).json()
        logging.info(await api.send(event.group_openid,
                       message = f"今天的菜单是{data['meal1']}，{data['meal2']}哦~"))
