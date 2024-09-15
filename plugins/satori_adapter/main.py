import aiohttp
import logging
import json

from peanut_bot.manager import load_config, plugin
from peanut_bot.driver.http import QOpenApi, HTTPDriver
from peanut_bot.utils.event import AtMessageEvent


from .onebotv11 import ob11_adapter
from .onebotv11 import ob11_http_server

satori_url: dict = load_config("./satori.cfg",{"url":"http://127.0.0.1:16385"})

class Satori_adapter_webhook(HTTPDriver):
    def __init__(self, satori_url: dict) -> None:
        super().__init__(satori_url["url"], headers={'Content-Type': 'application/json'})


satori_http_client = Satori_adapter_webhook(satori_url)

ob11_http_server.ob11_server_run()

@plugin
async def sac(api:QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    if event.content.startswith('/sac'):
        event.content = event.content[5:]
        ob11_http_server.api = api
        ob11_http_server.event = event
        response = await satori_http_client.post_async(data = ob11_adapter.parser(event).raw_data)
        # logging.info(response)
        # await api.send(event,message=str(response))
    


