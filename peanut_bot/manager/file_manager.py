import sys
import os
import aiofiles
import filelock

print(f"{__file__}")

running_path = os.path.abspath(sys.argv[0])

def load(path: str):
    '''
    params: path
    path 为
    '''

import os
import json
import sys
import filelock
import fcntl
path = os.getcwd().replace('\\','/')+'/'

def get_current_path(target=''):
    return path + str(target)

def save(data,path) -> None:
    with open(path,'w',encoding='utf-8') as f:
        try:
            f.write(json.dumps(data,ensure_ascii=True,indent=4))
        except:
            f.write(str(data))
        

def load(path,default = None) -> dict or str:
    ans = default
    if not os.path.exists(path):
        if default != None:
            save(default,path)
        return ans
    with open(path,'r',encoding='utf-8') as f:
        ans = f.read()
        try:
            ans = json.loads(ans)
        finally:
            pass
    return ans

def save_data(data,filename = None) -> None:
    name = sys._getframe(1).f_code.co_filename.split('/')[-1][:-3]
    savepath = f'{path}data/{name}/{filename if filename != None else "data.txt"}'
    print(f'saving data into {savepath}')
    if not os.path.exists(f'{path}data/{name}/'):
        os.mkdir(f'{path}data/{name}/')
    save(data,savepath)

def load_data(filename = None,default = None) -> dict or str:
    name = sys._getframe(1).f_code.co_filename.split('/')[-1][:-3]
    loadpath = f'{path}data/{name}/{filename if filename != None else "data.txt"}'
    print(f'loading data from {loadpath}')
    if not os.path.exists(f'{path}data/{name}/'):
        os.mkdir(f'{path}data/{name}/')
    return load(loadpath,default)

def save_config(data,filename = None) -> None:
    name = sys._getframe(1).f_code.co_filename.split('/')[-1][:-3]
    savepath = f'{path}config/{name}/{filename if filename != None else "config.txt"}'
    print(f'saving config into {savepath}')
    if not os.path.exists(f'{path}config/{name}/'):
        os.mkdir(f'{path}config/{name}/')
    save(data,savepath)

def load_config(filename = None,default = None) -> dict or str:
    name = sys._getframe(1).f_code.co_filename.split('/')[-1][:-3]
    loadpath = f'{path}config/{name}/{filename if filename != None else "config.txt"}'
    print(f'loading config from {loadpath}')
    if not os.path.exists(f'{path}config/{name}/'):
        os.mkdir(f'{path}config/{name}/')
    return load(loadpath,default)

def save_cache(data,filename = None) -> None:
    name = sys._getframe(1).f_code.co_filename.split('/')[-1][:-3]
    savepath = f'{path}cache/{name}/{filename if filename != None else "cache.txt"}'
    print(f'saving cache into {savepath}')
    if not os.path.exists(f'{path}cache/{name}/'):
        os.mkdir(f'{path}cache/{name}/')
    save(data,savepath)

def load_cache(filename = None,default = None) -> dict or str:
    name = sys._getframe(1).f_code.co_filename.split('/')[-1][:-3]
    loadpath = f'{path}cache/{name}/{filename if filename != None else "cache.txt"}'
    print(f'loading cache from {loadpath}')
    if not os.path.exists(f'{path}cache/{name}/'):
        os.mkdir(f'{path}cache/{name}/')
    return load(loadpath,default)