# coding = utf-8
import sys
import json

sys.path.append('..')
from mcstatus import JavaServer
import logging

from peanut_bot.manager import plugin
from peanut_bot.utils import GroupAtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def ping(api:QOpenApi,event: GroupAtMessageEvent):
    if not isinstance(event,GroupAtMessageEvent):
        return
    try:
        with open('data/server_ip.json', 'r') as file:
            pass
    except:
        with open('data/server_ip.json', 'w') as file:
            data = {'default': 'svi.arrowss.top'}
            json.dump(data, file)
    if event.content.startswith(' /pinghelp') or event.content.startswith('/pinghelp'):
        help_message = (
                        '\n使用[/ping]查询默认服务器状态'
                        '\n使用[/ping <server>]查询指定服务器状态'
                        '\n使用[/pingset <server>]设置默认服务器'
                        '\n使用[/pingadd <name> <server>]添加服务器别名'
                        '\n使用[/pingdel <name>]删除服务器别名'
                        '\n使用[/pinglist]查看服务器列表'
                        '\n使用[/pingrelist]清理异常服务器别名')
        await api.send(event,
                       message=f'{help_message}')
    elif event.content.startswith(' /pingset') or event.content.startswith('/pingset'):
        with open('data/server_ip.json', 'r') as file:
            data = json.load(file)
        with open('data/server_ip.json', 'w') as file:
            data['default'] = event.content.split(" ")[-1]
            json.dump(data, file)
        await api.send(event,
                       message=f'默认服务器修改成功！')
    elif event.content.startswith(' /pingadd') or event.content.startswith('/pingadd'):
        name=event.content.split(" ")[-2]
        ip=event.content.split(" ")[-1]
        with open('data/server_ip.json', 'r') as file:
            data = json.load(file)
        if name in data:
            await api.send(event,
                           message=f'服务器别名{name}已存在，请先删除再添加。')
        else:
            if "." in name:
                await api.send(event,
                               message=f'服务器别名违规！')
            else:
                with open('data/server_ip.json', 'w') as file:
                    data[name] = ip
                    json.dump(data, file)
                await api.send(event,
                               message=f'已将服务器别名{name}添加')
    elif event.content.startswith(' /pingdel') or event.content.startswith('/pingdel'):
        name = event.content.split(" ")[-1]
        with open('data/server_ip.json', 'r') as file:
            data = json.load(file)
        if name in data and name != 'default':
            with open('data/server_ip.json', 'w+') as file:
                del data[name]
                json.dump(data, file)
            await api.send(event,
                           message=f'已将服务器别名{name}删除。')
        else:
            await api.send(event,
                           message=f'服务器别名{name}不存在！')
    elif event.content.startswith(' /pinglist') or event.content.startswith('/pinglist'):
        with open('data/server_ip.json', 'r') as file:
            data = '\n' + '\n'.join(list(json.load(file).keys()))
        await api.send(event,
                       message=f'当前服务器别名有：{data}')
    elif event.content.startswith(' /pingrelist') or event.content.startswith('/pingrelist'):
        with open('data/server_ip.json', 'r') as file:
            data = json.load(file)
        for i in data.copy():
            logging.info(i)
            if ping_ip(data[i])=="服务器地址有问题或服务器已经离线！":
                del data[i]
        with open('data/server_ip.json', 'w') as file:
            json.dump(data, file)
        await api.send(event,
                       message=f'异常服务器别名已清理')
    elif event.content.startswith(' /ping') or event.content.startswith('/ping'):
        if event.content.split(" ")[-1]=='/ping':
            with open('data/server_ip.json', 'r') as file:
                ip = json.load(file)['default']
            await api.send(event,
                           message=f'{ping_ip(ip)}')
        else:
            if '.' in event.content.split(" ")[-1]:
                await api.send(event,
                           message=f'{ping_ip(event.content.split(" ")[-1])}')
            else:
                with open('data/server_ip.json', 'r') as file:
                    ip = json.load(file)[event.content.split(" ")[-1]]
                await api.send(event,
                               message=f'{ping_ip(ip)}')
def ping_ip(ip):
    try:
        server = JavaServer.lookup(ip)
        status = vars(server.status())['raw']
    except:
        return "服务器地址有问题或服务器已经离线！"
    flag = True
    for k,v in status.items():
        if k not in ['version','players','description','favicon','onforcesSecureChat','previewsChat']:
            flag = False
        else:
            flag = True
    print(f'flag is {flag}')
    m_players = status['players']['max']
    n_players = status['players']['online']
    game_version = status['version']['name']
    ##    motd=status['description']['translate']
    motd = status['description'] if type(status['description']) == str else status['description'].get('text')
    #腾讯不给发链接
    server_message=f'\n服务器地址：{"_".join(ip.split("."))}\n描述：{motd}\n是否原版：{"是" if flag else "否"}\n游戏版本：{game_version}\n人数： ({n_players}/{m_players})'
    return  server_message


    
