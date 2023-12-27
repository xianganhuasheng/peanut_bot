#coding = utf-8

import os
import sys
import logging

import asyncio
from selenium import webdriver as wd
from selenium.webdriver.edge.options import Options
import base64
from io import BytesIO
from PIL import Image
from playwright.async_api import async_playwright

from peanut_bot.manager import plugin, load_config
from peanut_bot.utils import AtMessageEvent
from peanut_bot.driver import QOpenApi

PIC = os.path.join(sys.path[0],'pics')

@plugin
async def mcwiki(api: QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return   
    if event.content.startswith("/mcwiki"):
        logging.info("asking wiki")
        async with async_playwright() as playwright:
            logging.info('------init options------')
            searching_data = event.content[8:]
            logging.info(searching_data)
            webkit = playwright.webkit # or "firefox" or "webkit".
            browser = await webkit.launch()
            page = await browser.new_page()
            logging.info('------searching results------')
            logging.info(r"https://zh.minecraft.wiki/w/"+searching_data)
            await page.goto(r"https://zh.minecraft.wiki/w/"+searching_data)
            logging.info('------------taking screenshot------------')
            await page.screenshot(path=os.path.join(PIC,f'{event.author["id"]}_mcwiki.jpg'),full_page=True,type='jpeg',quality=33)
            await browser.close()
            logging.info('everything done')
            logging.info(f'{load_config("./imgserver.cfg")["host:port_for_tencent"]}img/{event.author["id"]}_mcwiki.jpg')
            await api.send_img(event,f'{load_config("./imgserver.cfg")["host:port_for_tencent"]}img/{event.author["id"]}_mcwiki.jpg')
            await browser.close()

    return True
