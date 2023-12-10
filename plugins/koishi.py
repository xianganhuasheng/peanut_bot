import logging
import random

from peanut_bot.manager.plugin_manager import plugin
from peanut_bot.driver.http import QOpenApi
from peanut_bot.utils.event import GroupAtMessageEvent


@plugin
async def koishi(api: QOpenApi,event: GroupAtMessageEvent):
    if not isinstance(event,GroupAtMessageEvent):
        return
    '''
    还没有写好文件处理部分，如果依靠全局变量的话程序关闭就没有保留了
    考虑学习数据库
    '''
    if event.content in ["koishi"," koishi"]:
        file_info = (await api.get_img_info(event.group_id,"https://koishi.js.org/koishi.png"))["file_info"]
        logging.info(await api.send_img(event.group_openid,file_info))