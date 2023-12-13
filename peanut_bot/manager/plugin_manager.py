import os
import sys
import importlib
import logging

from ..bot.bot import Bot
from ..utils import Event

class Plugins:
    '''
    插件管理类，有一个全局插件列表，bot会默认调用
    '''
    plugin_list = []

    def __init__(self,
                 name: str,
                 description: str,
                 author: str):
        self.name: str  = name
        self.description: str = description
        self.author: str = author
        self.actions = []
    def on_event(event: Event):
        pass

def plugin(func):
    Bot.plugin_list.append(func)
    logging.info(f'Loaded plugin: {func.__name__}')
    return func


def load_plugin(directory: str = "plugins") -> None:
    # 获取插件脚本所在的目录
    plugins_directory = os.path.join(sys.path[0], directory)
    # 如果directory是plugins，也就是第一次调用，则清空Bot的插件列表
    if directory == "plugins":
        if os.path.exists(plugins_directory) is False:
            os.mkdir(plugins_directory)
        Bot.plugin_list.clear()
    # 遍历 plugins 文件夹中的所有文件
    for filename in os.listdir(plugins_directory):
        full_path = os.path.join(plugins_directory, filename)
        if os.path.isdir(full_path):
            try:
                  load_plugin(directory = os.path.join(directory,filename))
            except Exception as e:
                logging.error(f"Failed to import module {module_path}: {e}")
        if filename.endswith(".py") and filename != "__init__.py":
            # 确保是 Python 文件并且不是特殊文件（比如 __init__.py）
            # 构建模块的完整路径
            prepath = ".".join(directory.split(os.path.sep))
            module_path = f"{prepath}.{filename[:-3]}"
            # 动态导入模块
            try:
                # logging.info(f"trying to load {module_path}")
                if module_path in sys.modules:
                    importlib.reload(sys.modules.get(module_path))
                else:
                    importlib.import_module(module_path)
                # print(f"Imported module: {module_path}")
            except Exception as e:
                logging.error(f"Failed to import module {module_path}: {e}")

