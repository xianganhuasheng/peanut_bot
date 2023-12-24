import asyncio
import logging
from .bot import Bot
from .manager import load_config
from .manager import load_plugin
from .pic_server import img_server_run

logging.basicConfig(level=logging.INFO,
format='[%(asctime)s] - %(filename)s in <line:%(lineno)d> - %(levelname)s: %(message)s')

BOT_LIST = load_config('./qbot.cfg')
IMAGE_SERVER = load_config('./imgserver.cfg')

def load_bot():
    load_plugin()
    bot_gather = []
    img_server_run(**IMAGE_SERVER)
    if isinstance(BOT_LIST,list):
        for config in BOT_LIST:
            bot_gather.append(Bot(**config).start())
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*bot_gather))
        asyncio.get_event_loop().run_forever()
    elif isinstance(BOT_LIST,dict):
        Bot(**BOT_LIST).run()



def bot():
    load_plugin()
    return Bot(**load_config('./qbot.cfg'))


if __name__ == "__main__":
    print(load_config('./qbot.cfg'))
    bot = Bot(**load_config('./qbot.cfg'))
    bot.run()