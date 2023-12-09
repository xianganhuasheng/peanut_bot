from peanut_bot.manager import plugin
from peanut_bot.driver import QOpenApi
from peanut_bot.utils import GroupAtMessageEvent
from peanut_bot.manager import load_plugin


@plugin
async def reload(api: QOpenApi,event: GroupAtMessageEvent):
    if not isinstance(event,GroupAtMessageEvent):
        return
    '''
    还没有写好文件处理部分，如果依靠全局变量的话程序关闭就没有保留了
    考虑学习数据库
    '''
    if event.content in ["reload",'更新插件',' reload',' 更新插件']:
        load_plugin()
        await api.send(event.group_openid,
                       message=f'更新完成')