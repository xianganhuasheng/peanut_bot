import sys
import os
import asyncio
import logging


import re

from aiohttp import web 
from aiohttp.web_request import Request 


from peanut_bot.driver.http import QOpenApi
from peanut_bot.utils import GroupAtMessageEvent

api:QOpenApi = None
event:GroupAtMessageEvent = None

routes = web.RouteTableDef()

from aiohttp.web_request import Request

@routes.get('/send_msg')
async def hello(request: Request):
    try:
        # 解析查询参数
        query = request.query
        message_type = query.get('message_type', [None])
        group_id = query.get('group_id', [None])
        message = query.get('message', [None])
        logging.info(f"Received message_type: {message_type}")
        logging.info(f"Received group_id: {group_id}")
        logging.info(f"Received message: {message}")
        message = remove_cq_at(message)
        logging.info(f"Received message: {message}")
        logging.info(f"Current api: {api}")
        logging.info(f"Current event: {event}")
        # 检查必要的参数是否存在
        if not message_type or not group_id or not message:
            logging.error("Missing parameters in request")
            return web.Response(status=400, text="Missing parameters")

        # 使用 api 发送消息
        if message_type == "group":
            await api.send(event=event, message=message)
            return web.Response(status=200, text="Message sent")
        else:
            return web.Response(status=400, text="Unsupported message type")

    except Exception as e:
        logging.error(f"Error handling request: {e}")
        return web.Response(status=500, text="Internal server error")


async def main(host,port):
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    while True:
        await asyncio.sleep(3600)


# def parser_cq(message:str):
#     if "[CQ:at" in message:


def remove_cq_at(text: str) -> str:
    # 定义正则表达式，匹配 [CQ:at,qq=任意数值]
    pattern = r'\[CQ:at,qq=[0-9A-Fa-f]+]'
    # 使用 re.sub 替换匹配的部分为空字符串
    return re.sub(pattern, '', text)




def ob11_server_run(host="0.0.0.0",port="5700",**_):
    if asyncio.get_event_loop() is None:
        loop = asyncio.new_event_loop()
    loop = asyncio.get_event_loop()
    loop.create_task(main(host,port))


if __name__ == "__main__":
    ob11_server_run()
    asyncio.get_event_loop().run_forever()
