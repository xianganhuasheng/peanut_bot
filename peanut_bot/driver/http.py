import json
import aiohttp
import requests
import asyncio

import logging

from ..utils import Event,GroupAtMessageEvent,GuildAtMessageEvent

class HTTPDriver:
    '''
    纯正http，不掺杂一点QQ信息
    '''
    def __init__(self,url: str,headers: str = None) -> None:
        self.url = url
        self.headers = headers


    async def get_async(self,params: str | dict = None, suffix: str = "", **kwargs) -> dict:
        if isinstance(params,dict):
            params = json.dumps(params)
        async with aiohttp.ClientSession(headers=self.headers, **kwargs) as client:
            async with client.get(params = params if params is not None else '',url = f'{self.url}{suffix}') as respond:
                return await respond.json()
    

    async def post_async(self,data: str | dict = None, suffix: str = "", **kwargs) -> dict:
        if isinstance(data,dict):
            data = json.dumps(data)
        async with aiohttp.ClientSession(headers=self.headers, **kwargs) as client:
            async with client.post(data = data,url = f'{self.url}{suffix}') as respond:
                try:
                    return await respond.json()
                except:
                    return await respond.text()

    def get_sync(self,params: str | dict = None, suffix: str = "", **kwargs) -> dict:
        if isinstance(params,dict):
            params = json.dumps(params)
        return requests.get(f'{self.url}{"" if suffix is None else suffix}',
                            params = params,
                            headers = self.headers,
                            **kwargs).json()
  
    def post_sync(self,data: str | dict = None, suffix: str = "", **kwargs) -> dict:
        if isinstance(data,dict):
            data = json.dumps(data)
        return requests.post(url = f'{self.url}{"" if suffix is None else suffix}',
                             data = data,
                             headers = self.headers,
                             **kwargs).json()


class QOpenApi(HTTPDriver):
    '''
    这个类为包含了QQ信息的OpenApi类
    tx每一段时间要更新一个access，不及时更新发不了东西
    使用hold_openapi维护与官方的OpenApi的Access
    '''

    # _instance = None

    # def __new__(cls, url: str, app_id: str, app_secret: str):
    #     if cls._instance is None:
    #         cls._instance = super(QOpenApi, cls).__new__(cls)
    #         super().__init__(url, {'Content-Type': 'application/json'})
    #         cls._instance.app_id = app_id
    #         cls._instance.app_secret = app_secret
    #         cls._instance.data = {
    #             "appId": f"{cls._instance.app_id}",
    #             "clientSecret": f"{cls._instance.app_secret}"
    #         }
    #         cls._instance.expires_in = 7200
    #         cls._instance.access = None
    #         cls._instance.driver = HTTPDriver('https://bots.qq.com/app/getAppAccessToken',  
    #                                           {'Content-Type': 'application/json'})
    #     return cls._instance


    def __init__(self,url: str,app_id: str,app_secret: str) -> None:
        super().__init__(url,{'Content-Type':'application/json'})        
        self.app_id = app_id
        self.app_secret = app_secret
        self.data = {
            "appId": f"{self.app_id}",
            "clientSecret": f"{self.app_secret}"
        }
        # openAPI part
        self.expires_in = 7200
        self.access = None
        self.driver = HTTPDriver('https://bots.qq.com/app/getAppAccessToken',
                                     {'Content-Type':'application/json'})

    async def get_access(self) -> None:
        '''
        获取Access并保存在实例里
        '''
        # 获取Access
        logging.info('start to get access')
        rpl = await self.driver.post_async(data = self.data)
        # print(rpl)
        try:
            self.access = rpl["access_token"]
            self.expires_in = int(rpl["expires_in"])
            self.headers = {
                                'Content-Type' : 'application/json',
                                'Authorization': f"QQBot {self.access}",
                                'X-Union-Appid': f"{self.app_id}",
                            }
            # self.driver.headers = self.headers
            logging.info(f"successfully get access")
            logging.debug(f"the Access info is:\nAccess:{self.access}\nexpires in {self.expires_in} s")
        except Exception as e:
            logging.error("Failed to get openApi access, something bad happend")
            logging.error(e.with_traceback())
            raise Exception
                    
    async def hold_openapi(self) -> None:
        '''
        内含while循环，用于保持Access一直有效，用asyncio.ensure_future或者create_task来调用
        '''
        while True:
            logging.info("begin to hold api")
            try:
                await self.get_access()
                logging.info(f'目前的Access将在{self.expires_in-30}秒后重新获取')
            except Exception as e:
                logging.debug(e.__traceback__)
                logging.info(f'目前的Access将在{self.expires_in-30}秒后重新获取')
            finally:
                await asyncio.sleep(abs(self.expires_in-30))
                

    async def update_latest_message_id(self,event:Event):
        '''
        主要是更新最后的id，后续考虑通过设计离开api部分，或者作为发消息所需要的id
        '''
        # logging.info(event.message_id)
        self.latest_message_id = event.message_id

    async def send(self,event,message=None) -> dict:
        # 发送消息的api，后续需要重新设计封装
        # 期望的形式是简便且好用，同时不需要太多东西
        # 例如，被动消息的话，需要的msg_id部分可以通过设计一个auto函数屏蔽掉
        if isinstance(event,GroupAtMessageEvent):
            fix = f'/v2/groups/{event.group_openid}/messages'
        elif isinstance(event,GuildAtMessageEvent):
            fix = f'/channels/{event.group_openid}/messages'
        data = {"content":'我服了，奶奶' if message is None else message,
                "msg_type":0,
                'msg_id':str(event.message_id)
                }
        # 调试用的log
        logging.debug(f'try to send{json.dumps(data)} to {self.url}{fix}\n with header: {self.headers}')
        await self.post_async(f'{self.url}{fix}')
        rpl = await self.post_async(data,fix)
        logging.debug(rpl)
        return rpl
            
    async def send_guild(self,channel_id,message = None) -> dict:
        fix = f'/channels/{channel_id}/messages'
        data = {"content":'我服了，奶奶' if message is None else message,
                'msg_id':str(self.latest_message_id)
                }
        logging.debug(f'try to send{json.dumps(data)} to {self.url}{fix}\n with header: {self.headers}')
        await self.post_async(f'{self.url}{fix}')
        rpl = await self.post_async(data,fix)
        logging.debug(rpl)
        return rpl

    async def get_img_info(self,event,fileurl) -> dict:
        if isinstance(event,GroupAtMessageEvent):
            fix = f'/v2/groups/{event.group_openid}/files'
        data = {
            "file_type": 1,
            "url": fileurl,
            "srv_send_msg": False
        }
        logging.debug(f'try to send{json.dumps(data)} to {self.url}{fix}\n with header: {self.headers}')
        await self.post_async(f'{self.url}{fix}')
        rpl = await self.post_async(data,fix)
        logging.debug(rpl)
        return rpl
    
    async def send_img(self,event,file_url):
        if isinstance(event,GroupAtMessageEvent):
            fix = f'/v2/groups/{event.group_openid}/messages'
            file_info = (await self.get_img_info(event,file_url))["file_info"]
            data = {"content":' ',
                "msg_type":7,
                'msg_id':str(event.message_id),
                "media": {
                    "file_info": file_info
                }
                }
        elif isinstance(event,GuildAtMessageEvent):
            fix = f"/channels/{event.channel_id}/messages"
            data = {"image":file_url,
                    "msg_id":str(self.latest_message_id)
                    }
        # 调试用的log
        logging.debug(f'try to send{json.dumps(data)} to {self.url}{fix}\n with header: {self.headers}')
        rpl = await self.post_async(data,fix)
        if str(rpl.get("code")) == 11263:
            rpl = await self.post_async(data,fix)
        logging.debug(rpl)
        return rpl


class API:
    def __init__(self,api) -> None:
        self.api = api

    async def send_message(self,target: str, message: str = None):
        await self.api.api_send(target,message)
        
