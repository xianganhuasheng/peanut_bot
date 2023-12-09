from peanut_bot.manager.plugin_manager import plugin
from peanut_bot.driver.http import QOpenApi
from peanut_bot.utils.event import GroupAtMessageEvent

from .core import main

@plugin
async def ba_query(api:QOpenApi,event: GroupAtMessageEvent):
    if event.content.startswith(" ba_raid") or event.content.startswith("ba_raid"):
        print("asking for ba")
        is_bili = 2 if event.content.find("-b") >= 8 else 1
        print(await api.send(event.group_openid, main(is_bili)))
