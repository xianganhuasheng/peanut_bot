# coding = utf-8
import sys
import requests

sys.path.append('..')
import logging


from peanut_bot.manager import plugin
from peanut_bot.utils import AtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def today_news(api:QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    if event.content.startswith(' /news') or event.content.startswith('/news'):
        url = "https://dayu.qqsuu.cn/weiyujianbao/apis.php?type=json"
        data = requests.get(url).json()["data"]
        logging.info(await api.send_img(event, data))

