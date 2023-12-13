# coding = utf-8
import sys
import requests

sys.path.append('..')
import logging


from peanut_bot.manager import plugin
from peanut_bot.utils import AtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def rua(api:QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    if event.content in ["/rua",'/摸头']:
        data = get_mo_tou_gif()
        logging.info(await api.send_img(event, data))
def get_mo_tou_gif(qq='2854213604'):
    api_url = 'https://api.52vmy.cn/api/avath/rua'
    params = {'qq':qq,  'type': 'JSON'}
    response = requests.get(api_url, params=params)
    return response.json()['url']

