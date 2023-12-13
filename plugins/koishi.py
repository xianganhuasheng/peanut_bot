import logging
import random

from peanut_bot.manager.plugin_manager import plugin
from peanut_bot.driver.http import QOpenApi
from peanut_bot.utils.event import AtMessageEvent


@plugin
async def koishi(api: QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    '''
    还没有写好文件处理部分，如果依靠全局变量的话程序关闭就没有保留了
    考虑学习数据库
    '''
    if event.content in ["koishi"," koishi"]:
        logging.info(await api.send_img(event,"https://koishi.js.org/koishi.png"))
