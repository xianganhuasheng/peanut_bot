import sys
import os
import asyncio


from aiohttp import web 
from aiohttp.web_request import Request 


#检查文件路径是否存在
PATH = os.path.abspath(sys.path[0])
if not os.path.exists(os.path.join(PATH,"pics")):
    os.mkdir(os.path.join(PATH,"pics"))
print(PATH)


# logger = logging.Logger("web",level=logging.INFO)
# handler = logging.FileHandler(f'{PATH}\\log.txt')
# logger.addHandler(handler)


routes = web.RouteTableDef()

@routes.get('/img/{file_path}')
async def hello(request:Request):
    text = request.match_info.get("file_path","peanut")
    # logger.error(os.path.join(PATH,text))
    # return web.Response(text = os.path.join(PATH,text))
    if os.path.exists(file := os.path.join(PATH,'pics',text)):
        return web.FileResponse(file)
    else:
        raise web.HTTPNotFound()


async def main(host,port):
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    while True:
        await asyncio.sleep(3600)


def img_server_run(host="0.0.0.0",port="11451",**_):
    if asyncio.get_event_loop() is None:
        loop = asyncio.new_event_loop()
    loop = asyncio.get_event_loop()
    loop.create_task(main(host,port))


if __name__ == "__main__":
    img_server_run()
    asyncio.get_event_loop().run_forever()


