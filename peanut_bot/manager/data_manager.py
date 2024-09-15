import sys
import os
import json
import logging

src_path = sys.path[0]

def load_config(path: str, default = None) -> dict | list:
    # 还没写好的，加载本地config文件，使用json，
    if os.path.exists(path):
        if os.path.isfile(path):
            with open(path,'r') as f:
                config = json.load(f)
                return config
        else:
           logging.error('config path must be file')
    else:
        if default == None:
            default = [{
                         "Qid" : "your bot's QQ",
                        "AppID" : "your bot's appid",
                        "Token" : "your bot's token",
                        "AppSecret" : "your bot's appsecret",
                        "is_sandbox" : True 
                      }]
        # 缺个一路补足路径文件夹的函数
        with open(path,'w') as f:
            json.dump(default,
                      f,
                      indent=4,
                      ensure_ascii=False)
            logging.info('already generate the config, please enter your data')
    input("enter any key to exit()")
    exit()

def make_config() -> None:
    pass