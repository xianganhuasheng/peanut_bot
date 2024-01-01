import abc
import asyncio
import json
import logging
import websockets
from websockets.exceptions import ConnectionClosed


class WebsocketDriver:
    '''
    纯正Websocket，不掺杂一点QQ信息
    '''
    def __init__(self,url: str,headers: str = None) -> None:
        self.url = url
        self.headers = headers

    @abc.abstractmethod
    async def run(self):
        '''
        保持Ws连接
        '''
        raise NotImplementedError
    
    async def connect(self) -> None:
        self.session = await websockets.connect(self.url)
        logging.info(f"successfully connect to {self.url}")

    async def send(self,payload: str or dict) -> None:
        if isinstance(payload,dict):
            payload = json.dumps(payload)
        await self.session.send(payload)
        logging.debug(f"successfully send {payload}")
    
    async def receive(self) -> dict:
        msg = json.loads(await self.session.recv())
        logging.debug(f"websocket receive message: {msg}")
        return msg


class QWebsocket(WebsocketDriver):
    def __init__(self, url: str,headers: str,token: str) -> None:
        super().__init__(url, headers)
        self.token = token
        self.latest_msg_id = 1

    async def connect(self) -> None:
        logging.info("starting websocket connection")
        await super().connect()
        rpl = await super().receive()
        self.heartbeat_cd = int(rpl["d"]["heartbeat_interval"]) / 1000
        logging.debug(f"the heartbeat cd is {self.heartbeat_cd}s")


    async def identify(self):
        # 官方定义的身份认证部分
        payload ={
        "op": 2,
        "d": {
            "token": self.token,
            # intents部分，后续会实现可以选择的事件订阅，目前是写死了的
            "intents": 0|1<<30|1<<1|1<<0|1<<25,
            "shard": [0, 1],
            "properties": {
            "$os": "linux",
            "$browser": "my_library",
            "$device": "my_library"
                }
            }
        }
        logging.info("trying to identify")
        await self.send(json.dumps(payload))
        rpl = await super().receive()
        logging.debug(f'Identifying gets reply: {rpl}')
        if rpl["d"] == False:
            return
        self.latest_msg_id = rpl["s"]
        self.Version = rpl["d"]["version"]
        self.SessionId = rpl["d"]["session_id"]
        self.User = rpl["d"]["user"]
        self.UserId = rpl["d"]["user"]["id"]
        self.UserName = rpl["d"]["user"]["username"]
        logging.info("Successfully Identified")


    async def bot_heartbeat(self):
        # 一直心跳维持
        payload = {
            "op":1,
            "d":self.latest_msg_id
        }
        while True:
            await self.send(payload)
            await asyncio.sleep(self.heartbeat_cd)


    async def receive(self,func:asyncio.coroutines) -> dict:
        '''
        将bot中的一个消息处理函数绑定进来
        '''
        while True:
            message = await super().receive()
            if message.get("s") is not None:
                self.latest_msg_id = message["s"]
            await func(message)


    async def run(self,func) -> None:
        # 官方的重连机制不会写，目前是ws直接扬了再重连
        # 不过由于个人需求，官方的重连机制可能也不会支持
        logging.info("start to run the websocket client")
        self.count = 0
        while True:
            try:
                # 不知道他的wss是一直一样还是偶尔会变，反正封进来了
                while True:
                    try:
                        # 顺序执行，先用connect完成连接，再开始recv
                        # 避免异步执行顺序导致问题
                        await self.connect()
                        await self.identify()
                        asyncio.ensure_future(self.bot_heartbeat())
                        await self.receive(func)
                    except ConnectionClosed as e:
                        cd = 10
                        logging.exception(e,exc_info=False)
                        if e.code in range(4900,4914):
                            logging.info(f"服务器内部错误，{cd}秒后尝试重连")
                            await asyncio.sleep(cd)
                            logging.info("尝试重新连接到服务器")
                            continue
                        elif e.code in (4008,4009):
                            logging.info(f"{cd}")
                            await asyncio.sleep(cd)
                            logging.info("尝试重新连接到服务器")
                            continue
                        elif e.code in (4006,4007):
                            logging.info(f"服务器内部错误，{cd}秒后尝试重连")
                            await asyncio.sleep(cd)
                            logging.info("尝试重新连接到服务器")
                            continue
                        else:
                            break
            except ConnectionRefusedError as e:
                logging.exception(e)
                if self.count == 10: 
                    return
                self.count += 1
                await asyncio.sleep(5)
            finally:
                self.session.close()



