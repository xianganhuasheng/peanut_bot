import logging


from ..utils import Event, GroupAtMessageEvent, GuildAtMessageEvent


class Plugin:
    '''
    插件类
    还未实现
    '''


    def __init__(self,
                 name: str = "undefined",
                 description: str = "no description",
                 author: str = "unknown"):
        self.name: str  = name
        self.description: str = description
        self.author: str = author
        self.actions: dict[type:list[function]] = {}
        self.event_set = set()
        

    def act(self,event: Event):
        if func_list := self.actions.get(type(event)):
            for func in func_list:
                try:
                    func(event)
                except Exception as e:
                    logging.error(e.args)

    def on_event(self,event_type: type, func):
        self.event_set.add(event_type)
        if func_list := self.actions.get(event_type):
            func_list.append(func)
        else:
            self.actions.update({event_type:[func]})


    def on_at_message(self,*prefix: str, **_):
        def deco(func):
            self.on_event(self,GroupAtMessageEvent,func)
            self.on_event(self,GuildAtMessageEvent,func)
            return func
        return deco


    def on_group_at_message(self,*prefix: str, **_):
        def deco(func):
            self.on_event(self,GroupAtMessageEvent,func)
            return func
        return deco


    def on_guild_at_message(self,*prefix: str, **_):
        def deco(func):
            self.on_event(self,GuildAtMessageEvent,func)
            return func
        return deco
