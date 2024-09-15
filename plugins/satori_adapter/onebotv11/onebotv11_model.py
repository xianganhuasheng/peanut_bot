'''base on onebotv11'''


EVENT_TYPES = ('message','notice','request','meta_event')


class Ob11Event:
    '''
    OneBot v11 事件基类
    '''
    def __init__(self,ob11_data: dict) -> None:
        self.raw_data: dict = ob11_data
        self.time: int = ob11_data.get('time')
        self.self_id: int = ob11_data.get('self_id')
        self.post_type: str = ob11_data.get('post_type')
        if self.time is None or self.self_id is None or self.post_type is None:
            raise ValueError('the data seem to be not a ob11event,please check')
        
    def __getitem__(self, key):  
        # 尝试通过点号访问属性  
        if not isinstance(key, str):  
            raise TypeError("Keys must be strings")  
        try:  
            return getattr(self, key)  
        except AttributeError:  
            # 如果属性不存在，可以抛出一个 KeyError（可选）  
            raise KeyError(f"Key '{key}' not found")  
  
    def __setitem__(self, key, value):  
        # 设置属性  
        if not isinstance(key, str):  
            raise TypeError("Keys must be strings")  
        setattr(self, key, value)  

    def get(self,key):
        return self.__getitem__(key)



def ob11_parser(ob11_data: dict):
    if ob11_data['post_type'] == 'message':
        if ob11_data['message_type'] == 'group':
            return Ob11GroupMessageEvent(ob11_data=ob11_data)
        elif ob11_data['message_type'] == 'private':
            return Ob11PrivateMessageEvent(ob11_data=ob11_data)

    elif ob11_data['post_type'] == 'notice': 
        if ob11_data['notice_type'] == 'group_upload':
            return Ob11GroupUploadNoticeEvent(ob11_data=ob11_data)
        elif ob11_data['notice_type'] == 'group_admin':
            return Ob11GroupAdminNoticeEvent(ob11_data=ob11_data)
        elif ob11_data['notice_type'] == 'group_decrease':
            return Ob11GroupDecreaseNoticeEvent(ob11_data=ob11_data)
        elif ob11_data['notice_type'] == 'group_increase':
            return Ob11GroupIncreaseNoticeEvent(ob11_data=ob11_data)
        elif ob11_data['notice_type'] == 'group_ban':
            return Ob11GroupBanNoticeEvent(ob11_data=ob11_data)
        elif ob11_data['notice_type'] == 'friend_add':
            return Ob11FriendAddNoticeEvent(ob11_data=ob11_data)
        elif ob11_data['notice_type'] == 'group_recall':
            return Ob11GroupRecallNoticeEvent(ob11_data=ob11_data)
        elif ob11_data['notice_type'] == 'friend_recall':
            return Ob11FriendRecallNoticeEvent(ob11_data=ob11_data)
        elif ob11_data['notice_type'] == 'notify':
            if ob11_data['sub_type'] == 'poke':
                return Ob11NotifyPokeNoticeEvent(ob11_data=ob11_data)
            elif ob11_data['sub_type'] == 'lucky_king':
                return Ob11NotifyLuckyKingNoticeEvent(ob11_data=ob11_data)
            elif ob11_data['sub_type'] == 'honor':
                return Ob11NotifyHonorNoticeEvent(ob11_data=ob11_data)

    elif ob11_data['post_type'] == 'request':
        if ob11_data['request_type'] == 'group':
            if ob11_data['sub_type'] == 'add':
                return Ob11GroupAddRequestEvent(ob11_data=ob11_data)
            elif ob11_data['sub_type'] == 'invite':
                return Ob11GroupInviteRequestEvent(ob11_data=ob11_data)
        elif ob11_data['request_type'] == 'friend':
            return Ob11FriendRequestEvent(ob11_data=ob11_data)

    elif ob11_data['post_type'] == 'meta_event':
        if ob11_data['meta_event_type'] == 'lifecycle':
            return Ob11MetaLifeCycleEvent(ob11_data=ob11_data)
        elif ob11_data['meta_event_type'] == 'heartbeat':
            return Ob11MetaHeartBeatEvent(ob11_data=ob11_data)

'''MessageEvent'''


class Ob11MessageEvent(Ob11Event):
    '''
    Onebot v11 消息事件基类
    '''
    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.post_type: str = 'message'
        self.message_type: str = ob11_data['message_type']
        self.sub_type: str = ob11_data['sub_type']
        self.message_id: int = ob11_data['message_id']
        self.user_id: str = ob11_data['user_id']
        self.message: str = ob11_data['message']
        self.raw_message: str = ob11_data['raw_message']
        self.font: int = ob11_data['font']
        self.sender: Sender = Sender(ob11_data['sender'])


class Ob11PrivateMessageEvent(Ob11MessageEvent):
    '''
    Onebot v11 私聊消息事件类
    '''
    sub_type_list = ('friend','group','other') 

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)


class Ob11GroupMessageEvent(Ob11MessageEvent):
    '''
    Onebot v11 群聊消息事件类
    '''
    sub_type_list = ('normal','anonymous','notice')

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.group_id: str = ob11_data['group_id']
        self.anonymous: bool = ob11_data.get('anonymous',None)
        

class Sender():
    '''
    消息事件 发送者类
    '''
    def __init__(self,sender_data: dict) -> None:
        self.user_id: int = sender_data.get('user_id', None)  # 需要指定一个默认值，例如 0 或 None，取决于逻辑需求  
        self.nickname: str = sender_data.get('nickname', '')  # 对于字符串，通常使用空字符串作为默认值  
        self.card: str = sender_data.get('card', '')  
        self.sex: str = sender_data.get('sex', '')  
        self.age: int = sender_data.get('age', 0)  # 同样需要指定一个默认值，例如 0  
        self.area: str = sender_data.get('area', '')  
        self.level: str = sender_data.get('level', '')  
        self.role: str = sender_data.get('role', '')  
        self.title: str = sender_data.get('title', '')


'''MetaEvent'''


class Ob11MetaEvent(Ob11Event):
    '''
    Onebot v11 元事件基类
    '''
    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.meta_event_type: str = ob11_data['meta_event_type']


class Ob11MetaLifeCycleEvent(Ob11Event):
    '''
    Onebot v11 生命周期元事件类
    '''
    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.sub_type: str = ob11_data['sub_type']


class Ob11MetaHeartBeatEvent(Ob11Event):
    '''
    Onebot v11 心跳元事件类
    '''
    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.interval: str = ob11_data['interval']
        self.status: str = ob11_data['status']


'''RequestEvent'''


class Ob11RequestEvent(Ob11Event):
    '''
    Onebot v11 请求事件类
    '''
    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.request_type: str = ob11_data['request_type']
        self.comment: str = ob11_data['comment']
        self.flag: str = ob11_data['flag']
        

class Ob11FriendRequestEvent(Ob11RequestEvent):
    '''
    Onebot v11 加好友请求事件类
    '''
    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.user_id: int = ob11_data['user_id']

        
class Ob11GroupRequestEvent(Ob11RequestEvent):
    '''
    Onebot v11 群聊请求事件类
    '''
    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.sub_type: str = ob11_data['sub_type']
        self.group_id: int = ob11_data['group_id']
        self.user_id: int = ob11_data['user_id']


class Ob11GroupAddRequestEvent(Ob11GroupRequestEvent):
    '''
    Onebot v11 加群请求事件类
    '''
    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)


class Ob11GroupInviteRequestEvent(Ob11GroupRequestEvent):
    '''
    Onebot v11 邀请入群请求事件类
    '''
    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)



'''NoticeEvent'''


class Ob11NoticeEvent(Ob11Event):

    '''
    OneBot v11 通知事件基类
    '''

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.post_type: str = 'notice'
        self.notice_type: str = ob11_data['notice_type']
        self.sub_type: str = ob11_data['sub_type']
        self.user_id: str = ob11_data['user_id']

class Ob11GroupUploadNoticeEvent(Ob11NoticeEvent):
    '''
    Onebot v11 群文件上传通知事件类
    '''
    sub_type_list = ()

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.group_id: str = ob11_data['group_id']
        self.file: File = File(ob11_data['file'])



class Ob11GroupAdminNoticeEvent(Ob11NoticeEvent):
    '''
    Onebot v11 群管理员变动通知事件类
    '''
    sub_type_list = ('set','unset')

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.group_id: str = ob11_data['group_id']

class Ob11GroupDecreaseNoticeEvent(Ob11NoticeEvent):
    '''
    Onebot v11 群成员减少通知事件类
    '''
    sub_type_list = ('leave','kick','kick_me')

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.group_id: str = ob11_data['group_id']
        self.operator_id: str = ob11_data['operator_id']

class Ob11GroupIncreaseNoticeEvent(Ob11NoticeEvent):
    '''
    Onebot v11 群成员增加通知事件类
    '''
    sub_type_list = ('approve','invite')

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.group_id: str = ob11_data['group_id']
        self.operator_id: str = ob11_data['operator_id']

class Ob11GroupBanNoticeEvent(Ob11NoticeEvent):
    '''
    Onebot v11 群禁言通知事件类
    '''
    sub_type_list = ('ban','lift_ban')

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.group_id: str = ob11_data['group_id']
        self.operator_id: str = ob11_data['operator_id']
        self.duration: str = ob11_data['duration']


class Ob11FriendAddNoticeEvent(Ob11NoticeEvent):
    '''
    Onebot v11 好友添加通知事件类
    '''
    sub_type_list = ()

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)

class Ob11GroupRecallNoticeEvent(Ob11NoticeEvent):
    '''
    Onebot v11 群消息撤回通知事件类
    '''
    sub_type_list = ()

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.group_id: str = ob11_data['group_id']
        self.operator_id: str = ob11_data['operator_id']
        self.message_id: str = ob11_data['message_id']

class Ob11FriendRecallNoticeEvent(Ob11NoticeEvent):
    '''
    Onebot v11 好友消息撤回通知事件类
    '''
    sub_type_list = ()

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.message_id: str = ob11_data['message_id']


class Ob11NotifyNoticeEvent(Ob11NoticeEvent):
    '''
    Onebot v11 群内戳一戳\群红包运气王\群成员荣誉变更通知事件类
    '''
    sub_type_list = ('poke','lucky_king','honor')

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.group_id: str = ob11_data['group_id']

class Ob11NotifyPokeNoticeEvent(Ob11NotifyNoticeEvent):
    '''
    Onebot v11 群内戳一戳通知事件类
    '''

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.target_id: str = ob11_data['target_id']

class Ob11NotifyLuckyKingNoticeEvent(Ob11NotifyNoticeEvent):
    '''
    Onebot v11 群红包运气王通知事件类
    '''

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.target_id: str = ob11_data['target_id']

class Ob11NotifyHonorNoticeEvent(Ob11NotifyNoticeEvent):
    '''
    Onebot v11 群成员荣誉变更通知事件类
    '''
    honor_type_list = ('talkative','performer','emotion') # 荣誉类型，分别表示龙王、群聊之火、快乐源泉

    def __init__(self, ob11_data: dict) -> None:
        super().__init__(ob11_data)
        self.honor_type: str = ob11_data['honor_type']



class File:
    '''
    通知消息事件 文件类
    '''
    def __init__(self, file_data: dict) -> None:
        self.id: str = file_data.get('id', None)  # 文件ID
        self.name: str = file_data.get('name', None) # 文件名
        self.size: int = file_data.get('size', None) # 文件大小
        self.busid: int = file_data.get('busid', None) # 未知