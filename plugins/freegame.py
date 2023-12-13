# coding = utf-8
import sys
import requests

sys.path.append('..')
import logging


from peanut_bot.manager import plugin
from peanut_bot.utils import AtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def freegame(api:QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    if event.content.startswith('/game'):
        url = "https://api.pearktrue.cn/api/steamplusone/"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            name_list = []
            message, n = f"\n喜加一资讯\n查询时间:{data['time']}\n", 0
            for item in data['data']:
                n = n + 1
                name = item['name']
                if name in name_list:
                    break
                name_list.append(name)
                starttime = item['starttime']
                endtime = item['endtime']
                perpetual = item['perpetual']
                source = item['source']
                message = message + f"{n}.\n名称:{name}\n" \
                                    f"开始时间:{starttime}\n" \
                                    f"结束时间:{endtime}\n" \
                                    f"永久:{perpetual}\n" \
                                    f"来源:{source}\n"
        else:
            message="请求失败"
        await api.send(event,
                       message=f'{message}')

