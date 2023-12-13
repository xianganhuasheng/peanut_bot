# coding = utf-8
import sys
import requests
import json

sys.path.append('..')
import logging


from peanut_bot.manager import plugin
from peanut_bot.utils import AtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def city_weather(api:QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    if event.content.startswith("/w"):
        city=event.content.split(" ")[-1]
        try:
            message=get_weather(name_check(city))
            await api.send(event,
                           message=f'{message}')
        except:
            await api.send(event,
                           message=f'城市名称错误!')
def get_weather(city_code):
    url = f"https://www.haotechs.cn/ljh-wx/weather?adcode={city_code}"
    result=requests.get(url).json()["result"]
    weather = f"\n地区:{result['province']}{result['city']}" \
              f"\n天气:{result['weather']}" \
              f"\n温度:{result['temperature']}" \
              f"\n风向:{result['winddirection']}" \
              f"\n风力:{result['windpower']}" \
              f"\n湿度:{result['humidity']}" \
              f"\n报告时间:{result['reporttime']}"
    return weather
def name_check(city):
    with open('data/city_code.json', 'r') as file:
        data=json.load(file)
    if city in list(data.keys()):
        return data[city]
    elif city+"市" in list(data.keys()):
        return data[city+"市"]
    elif city+"区" in list(data.keys()):
        return data[city+"区"]
    elif city+"县" in list(data.keys()):
        return data[city+"县"]
    else:
        return data[city]
