# coding = utf-8
import sys
import requests
import json

sys.path.append('..')
import logging

from peanut_bot.manager import plugin
from peanut_bot.utils import GroupAtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def stock(api:QOpenApi,event: GroupAtMessageEvent):
    if not isinstance(event,GroupAtMessageEvent):
        return
    try:
        with open('data/stock_gp.json', 'r') as file:
            pass
    except:
        with open('data/stock_gp.json', 'w') as file:
            data = {'default':'sh000001'}
            json.dump(data, file)
    if event.content.startswith(' /stockhelp') or event.content.startswith('/stockhelp'):
        help_message = (
                        '\n使用[/stock]查询默认股票信息'
                        '\n使用[/stock <stock_gp>/<name>]查询指定股票信息'
                        '\n使用[/stockset <stock_gp>]设置默认股票'
                        '\n使用[/stockadd <name> <stock_gp>]添加股票别名'
                        '\n使用[/stockdel <name>]删除股票别名'
                        '\n使用[/stocklist]查看股票列表')
        await api.send(event.group_openid,
                       message=f'{help_message}')
    elif event.content.startswith(' /stockset') or event.content.startswith('/stockset'):
        with open('data/stock_gp.json', 'r') as file:
            data = json.load(file)
        stock_gp=event.content.split(" ")[-1]
        if get_stock_message(stock_gp) != "股票代码错误！":
            with open('data/stock_gp.json', 'w') as file:
                data['default'] = stock_gp
                json.dump(data, file)
            await api.send(event.group_openid,
                           message=f'默认股票修改成功！')
        else:
            await api.send(event.group_openid,
                           message=f'股票代码错误！')
    elif event.content.startswith(' /stockadd') or event.content.startswith('/stockadd'):
        name=event.content.split(" ")[-2]
        stock_gp=event.content.split(" ")[-1]
        with open('data/stock_gp.json', 'r') as file:
            data = json.load(file)
        if name in data:
            await api.send(event.group_openid,
                           message=f'股票别名{name}已存在，请先删除再添加。')
        else:
            if '.' in name:
                await api.send(event.group_openid,
                               message=f'股票别名违规！')
            else:
                if get_stock_message(stock_gp) != "股票代码错误！":
                    with open('data/stock_gp.json', 'w') as file:
                        data[name] = stock_gp
                        json.dump(data, file)
                    await api.send(event.group_openid,
                                   message=f'已将股票别名{name}添加')
                else:
                    await api.send(event.group_openid,
                                   message=f'股票代码错误！')
    elif event.content.startswith(' /stockdel') or event.content.startswith('/stockdel'):
        name = event.content.split(" ")[-1]
        with open('data/stock_gp.json', 'r') as file:
            data = json.load(file)
        if name in data and name != 'default':
            with open('data/stock_gp.json', 'w+') as file:
                del data[name]
                json.dump(data, file)
            await api.send(event.group_openid,
                           message=f'已将股票别名{name}删除。')
        else:
            await api.send(event.group_openid,
                           message=f'股票别名{name}不存在！')
    elif event.content.startswith(' /stocklist') or event.content.startswith('/stocklist'):
        with open('data/stock_gp.json', 'r') as file:
            data = json.load(file)
        message,n=str("当前记录的股票有：\n"),0
        for i in data:
            n=n+1
            stock_gp=data[i]
            message=message+f"{n}.[{i}]:{stock_gp}\n"
        await api.send(event.group_openid,
                       message=f'{message}')
    elif event.content.startswith(' /stock') or event.content.startswith('/stock'):
        if event.content.split(" ")[-1]=='/stock':
            with open('data/stock_gp.json', 'r') as file:
                stock_gp = json.load(file)['default']
            await api.send(event.group_openid,
                           message=f'{get_stock_message(stock_gp)}')
        else:
            name=event.content.split(" ")[-1]
            with open('data/stock_gp.json', 'r') as file:
                data = json.load(file)
            if '.' in name:
                await api.send(event.group_openid,
                           message=f'股票别名/代码错误！')
            else:
                if name in data:
                    await api.send(event.group_openid,
                                   message=f'{get_stock_message(data[name])}')
                else:
                    await api.send(event.group_openid,
                                   message=f'{get_stock_message(name)}')
def get_stock_message(gp):
    try:
        url = f"https://zj.v.api.aa1.cn/api/gupiao-01/?gp={gp}"
        data = requests.get(url).text.split("~")
        message = f"\n股票名字:{data[1]}" \
                  f"\n股票代码:{data[2]}" \
                  f"\n当前价格:{data[3]}" \
                  f"\n昨收:{data[4]}" \
                  f"\n今开:{data[5]}" \
                  f"\n成交量:{data[6]}({data_format(data[6])})手" \
                  f"\n成交额:{data[37]}({data_format(data[37])})元\n" \
                  f"涨跌:{data[31]}({data[32]}%)" \
                  f"\n最高:{data[33]}\n" \
                  f"最低:{data[34]}" \
                  f"\n总市值:{data[45]}亿元"
        return message
    except:
        return "股票代码错误！"

def data_format(data):
    l=len(data)
    if l >= 12:
        result= f"{data[:-11]}.{data[-11:-9]}万亿"
    elif l >= 8:
        result= f"{data[:-7]}.{data[-7:-5]}亿"
    elif l >= 4:
        result = f"{data[:-3]}.{data[-3:-1]}万"
    else:
        result = data
    return result