import logging
import random

from peanut_bot.manager import plugin
from peanut_bot.utils import AtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

# print("loaded")

food_list = ['煎鸡蛋','热可可','牛肉饼','熟鳕鱼片','熟鲑鱼片',
            '馅饼酥皮','甜浆果芝士派','巧克力派','蛋糕切片',
            '苹果派切片','甜浆果芝士派切片','巧克力派切片',
            '甜浆果曲奇','蜂蜜曲奇','混合沙拉','烧烤串','鸡蛋三明治',
            '鸡肉三明治','汉堡包','饺子','填馅马铃薯','碗装填馅南瓜',
            '米饭','牛肉炖','鸡肉汤','蔬菜汤','鱼肉炖','炒饭','南瓜汤',
            '烘焙鳕鱼炖','盘装蜜汁火腿','肉丸意面','羊排意面','蔬菜面',
            '牛排配土豆','盘装牧羊人派','蔬菜杂烩','鱿鱼墨面','香烤鲑鱼',
            '苹果派','熟鸡肉丁','下界沙拉','熟培根']

@plugin
async def eat_what(api:QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    if event.content.startswith('/吃什么'):
        logging.info("asking eating what")
        menu = ','.join(random.choices(food_list,k=3))
        logging.info(menu)
        logging.info(await api.send(event,
                       message = f"今天的菜单是{menu}哦~"))
"""        
@plugin
async def eat_what_for_guild(api:QOpenApi,event: GuildAtMessageEvent):
    if not isinstance(event,GuildAtMessageEvent):
        return
    flag = 0
    no_at_content = ""
    for char in event.content:
        if flag == 1:
            no_at_content += char
        if char == '>':
            flag = 1
        
    # print(no_at_content)
    if no_at_content.startswith('/吃什么') or no_at_content.startswith(' /吃什么'):
        logging.info("asking eating what")
        menu = ','.join(random.choices(food_list,k=3))
        logging.info(menu)
        logging.info(await api.send_guild(event.channel_id,
                       message = f"今天的菜单是{menu}哦~"))
"""
