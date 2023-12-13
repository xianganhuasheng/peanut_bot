import logging

class Event:
    '''
    事件基类，还没想好有什么通用的需求做成接口
    '''
    def __init__(self, payload: dict) -> None:
        # logging.info(payload)
        self.payload:dict = payload
        self.event_name:str = payload["t"]
        self.event_id:str = payload["id"]
        self.data:dict = payload["d"]
        
    

class AtMessageEvent(Event):
    '''
    @事件
    '''
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)
        self.message_id:str = None

class GroupAtMessageEvent(AtMessageEvent):
    '''
    群聊@事件，目前主要使用这个
    '''
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)
        self.author = self.data["author"]
        self.content:str = self.data["content"].strip()
        self.group_id:str  = self.data["group_id"]
        self.group_openid:str = self.data["group_openid"]
        self.message_id:str = self.data["id"]
        self.time:str = self.data["timestamp"]

class GuildAtMessageEvent(AtMessageEvent):
    '''
    频道@事件，目前主要使用这个
    '''
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)
        self.author:str = self.data["author"]
        self.content:str= self.data["content"].strip()
        self.guild_id:str = self.data["guild_id"]
        self.channel_id:str = self.data["channel_id"]
        self.message_id:str = self.data["id"]
        self.member = self.data["member"]
        self.mentions = self.data["mentions"]
        self.seq = self.data["seq"]
        self.seq_in_channel = self.data["seq_in_channel"]
        self.time = self.data["timestamp"]
