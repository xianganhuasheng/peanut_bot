import logging

import asyncio

from ..driver import QOpenApi, HTTPDriver
from ..driver.websocket import QWebsocket
from ..utils.event import Event, GroupAtMessageEvent, GuildAtMessageEvent


class Bot:
    '''
    中控部分
    包含WebSocket与OpenApi两个类

    WebSocket负责与txqq官方接口维持websocket连接
    主要为建立连接与心跳，在接收到信息后交由Bot对象解析。

    OpenApi负责与txqq官方接口进行http通信
    由于官方机制，需要花时间维护一个Access
    Bot在处理好收到的消息后使用OpenApi提供的方法发送消息。
    '''
    plugin_list = []
    def __init__(self,Qid:str,AppID:str,Token:str,AppSecret:str,is_sandbox = False,**_) -> None:
        # botInfo part
        self.qid = Qid
        self.app_id = AppID
        self.token = Token
        self.app_secret = AppSecret
        self.is_sandbox = is_sandbox
        self.final_token = f"Bot {self.app_id}.{self.token}"
        if self.is_sandbox is False:
            self.api_url = 'https://api.sgroup.qq.com'
        elif self.is_sandbox is True:
            self.api_url = 'https://sandbox.api.sgroup.qq.com'
        else:
            raise ValueError('is_sandbox should only be True or False')
        self.headers = {
            'Authorization': self.final_token
        }

        logging.info("start to hold openapi")
        # openapi driver
        self.openapi = QOpenApi(self.api_url,
                                self.app_id,
                                self.app_secret)

        self.wss_url = HTTPDriver(self.api_url,self.headers).get_sync(suffix = "/gateway")["url"]
        logging.debug(f"the wss_url is {self.wss_url}")

        # websocket driver
        self.websocket = QWebsocket(self.wss_url,
                                    self.headers,
                                    self.final_token)

        # plugins
        self.plugin_list:list = None

    async def _on_recieve(self,rpl: dict):
        # 根据"op"项解析消息类型
        # 后续将在 op == 0 即消息中使用自定义的插件进行处理
        if rpl["op"] == 11:
            logging.debug('successfully heartbeat')
        elif rpl["op"] == 0:
            #这部分还没有设计好
            # logging.info(rpl)
            self.latest_msg_index = rpl["s"]
            event = Event(rpl)
            if rpl["t"] == "GROUP_AT_MESSAGE_CREATE":
                event = GroupAtMessageEvent(rpl)
                logging.info(f"event: {event.event_name}; source:{event.group_openid}; content:{event.content}")
            elif rpl["t"] == "AT_MESSAGE_CREATE":
                event = GuildAtMessageEvent(rpl)
                logging.info(f"event: {event.event_name}; source:{event.group_openid}; content:{event.content} At {event.time}")
            else:
                logging.info(f"event: {event.event_name}; data:{event.data}")
                return
            await self.openapi.update_latest_message_id(event)
            try:
                for plugin in Bot.plugin_list:
                    await plugin(self.openapi,event)
            except Exception as e:
                logging.error(e)
            # await self.OpenApi.api_send(rpl)
            # func(event=GroupAtMessageEvent(rpl),bot=self)
            # await self.action

    def run(self) -> None:
        # 程序的主入口，启用后程序阻塞
        logging.info('Starting to run the bot')
        # asyncio，将WebSocket和OpenApi的这两个方法加到事件循环
        if asyncio.get_event_loop() is None:
            asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.ensure_future(self.websocket.run(self._on_recieve))
        asyncio.ensure_future(self.openapi.hold_openapi())
        # 进入事件循环并永久执行
        asyncio.get_event_loop().run_forever()
    
    async def start(self) -> asyncio.coroutines:
        logging.info(f'Starting to run the bot with id: {self.app_id}, qid: {self.qid}')
        if asyncio.get_event_loop() is None:
            asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.ensure_future(self.websocket.run(self._on_recieve))
        asyncio.ensure_future(self.openapi.hold_openapi())
