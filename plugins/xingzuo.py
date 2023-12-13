# coding = utf-8
import sys
import requests

sys.path.append('..')
import logging


from peanut_bot.manager import plugin
from peanut_bot.utils import GroupAtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def xingzuo(api:QOpenApi,event: GroupAtMessageEvent):
    if not isinstance(event,GroupAtMessageEvent):
        return
    if event.content in ["/xz",'/星座',' /xz',' /星座']:
        url = "https://dayu.qqsuu.cn/xingzuoyunshi/apis.php?type=json"
        data = requests.get(url).json()['data']
        logging.info(await api.get_img_info(event, data))
        file_info = (await api.get_img_info(event, data))["file_info"]
        logging.info(await api.send_img(event, file_info))

