import logging
import random

from peanut_bot.manager.plugin_manager import plugin
from peanut_bot.driver.http import QOpenApi
from peanut_bot.utils.event import GroupAtMessageEvent


@plugin
async def repeat(api: QOpenApi,event: GroupAtMessageEvent):
    if not isinstance(event,GroupAtMessageEvent):
        return
    '''
    还没有写好文件处理部分，如果依靠全局变量的话程序关闭就没有保留了
    考虑学习数据库
    '''
    if event.content in ["jrrp",'今日人品',' jrrp',' 今日人品']:
        jrrp = round(random.gauss(50,16)) % 100
        logging.info(jrrp)
        await api.send(event.group_openid,
                       message=f'今天的人品值为{jrrp}哦')