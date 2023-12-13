# coding = utf-8
import sys
import requests

sys.path.append('..')
import logging


from peanut_bot.manager import plugin
from peanut_bot.utils import AtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def xingzuo(api:QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    if event.content in ["/xz",'/星座',' /xz',' /星座']:
        url = "https://dayu.qqsuu.cn/xingzuoyunshi/apis.php?type=json"
        data = requests.get(url).json()['data']
        logging.info(await api.send_img(event, data))

