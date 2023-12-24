import logging
import random

from peanut_bot.manager import load_config, plugin
from peanut_bot.driver.http import QOpenApi
from peanut_bot.utils.event import AtMessageEvent


@plugin
async def test_img(api: QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    '''
    还没有写好文件处理部分，如果依靠全局变量的话程序关闭就没有保留了
    考虑学习数据库
    '''
    if event.content in ["logo"]:
        await api.send_img(event,f'{load_config("./imgserver.cfg")["host:port_for_tencent"]}img/logo.jpg')