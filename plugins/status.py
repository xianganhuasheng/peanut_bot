# coding = utf-8
import sys
import os
sys.path.append('..')
import psutil

import logging

from peanut_bot.manager import plugin
from peanut_bot.utils import AtMessageEvent, GuildAtMessageEvent
from peanut_bot.driver import QOpenApi

@plugin
async def ping(api:QOpenApi,event: AtMessageEvent):
    if not isinstance(type(event),AtMessageEvent):
        return
    if event.content in ['/状态', '/status', ' /状态', ' /status']:
        my_pid = get_pid("python.exe")[0].pid
        vm = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(percpu=False)
        du = psutil.disk_usage('/').percent
        mp = psutil.Process(my_pid).memory_percent()
        message = f"\n服务器状态:\n饱腹度：{vm}%\n脑力消耗：{cpu}%\n血量消耗：{du}%\n我吃了：{mp}%"
        await api.send(event,
                       message=message)
def get_pid(name):
    pids = psutil.process_iter()
    ans = []
    for pid in pids:
        if(pid.name() == name):
            ans.append(pid)
    return ans
