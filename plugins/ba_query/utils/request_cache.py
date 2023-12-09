import requests
import json
import subprocess
import threading

global_header = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",   
    "connection": "keep-alive",
    "host": "api.arona.icu",
    "origin": "https://arona.icu",
    "referer": "https://arona.icu",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
}

def resolve_response(res: requests.Response):
    '''
    pure

    return same response but decrypt data
    '''
    r = json.loads(res.text)
    if r["crypt"]:
        r["data"] = json.loads(subprocess.run(["node", "plugins/ba_query/index.js", r["data"]], stdout=subprocess.PIPE).stdout.decode('utf-8'))
    return r

class RequestCache:
    def __init__(self, url: str, time = 1200) -> None:
        self.url = url
        self.time = time
        self.timer: threading.Timer = None
        self.cacheing = False
        self.response = None

    def reset_cache(self):
        self.cacheing = False

    def get_response(self, force_update = False) -> dict:
        if self.cacheing and not force_update and self.response != None:
            return self.response
        
        if self.timer != None:
            self.timer.cancel()

        res = resolve_response(requests.get(self.url, headers=global_header))
        self.cacheing = True
        self.response = res
        self.timer = threading.Timer(self.time, self.reset_cache).start()
        return res