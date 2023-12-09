import asyncio
import logging
from .bot import Bot
from .manager import load_config
from .manager import load_plugin


logging.basicConfig(level=logging.INFO,
format='[%(asctime)s] - %(filename)s in <line:%(lineno)d> - %(levelname)s: %(message)s')


def load_bot():
    load_plugin()
    bot_list = load_config('./qbot.cfg')
    bot_gather = []
    if isinstance(bot_list,list):
        for config in bot_list:
            bot_gather.append(Bot(**config).start())
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*bot_gather))
        asyncio.get_event_loop().run_forever()
    elif isinstance(bot_list,dict):
        Bot(**bot_list).run()



def bot():
    load_plugin()
    return Bot(**load_config('./qbot.cfg'))


if __name__ == "__main__":
    print(load_config('./qbot.cfg'))
    bot = Bot(**load_config('./qbot.cfg'))
    bot.run()