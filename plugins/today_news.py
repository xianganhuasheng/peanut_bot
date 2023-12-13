# coding = utf-8
import sys
import requests

sys.path.append('..')
import logging


from peanut_bot.manager import plugin
from peanut_bot.utils import GroupAtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def today_news(api:QOpenApi,event: GroupAtMessageEvent):
    if not isinstance(event,GroupAtMessageEvent):
        return
    if event.content.startswith(' /news') or event.content.startswith('/news'):
        url = "https://dayu.qqsuu.cn/weiyujianbao/apis.php?type=json"
        data = requests.get(url).json()
        logging.info(await api.get_img_info(event, data))
        file_info = (await api.get_img_info(event, data))["file_info"]
        logging.info(await api.send_img(event, file_info))

