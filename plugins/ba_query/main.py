from peanut_bot.manager.plugin_manager import plugin
from peanut_bot.driver.http import QOpenApi
from peanut_bot.utils.event import AtMessageEvent

from .core import main

@plugin
async def ba_query(api:QOpenApi,event: AtMessageEvent):
    if event.content.startswith("/ba"):
        print("asking for ba")
        is_bili = 2 if event.content.find("-b") >= 3 else 1
        print(await api.send(event, main(is_bili)))
