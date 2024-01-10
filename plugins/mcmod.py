# coding=utf-8


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
async def mcmod(api: QOpenApi,event: AtMessageEvent):
    if not issubclass(type(event),AtMessageEvent):
        return
    if event.content.startswith('/mcmod'):
        asking = event.content[7:]
        edge_options = Options()
        edge_options.add_argument('headless')
        edge_options.add_argument('--no-sandbox')
        edge_options.add_argument('--disable-gpu')
        edge_options.add_argument('--hide-scrollbars')
        driver = wd.Edge(options = edge_options)#浏览器设置
        await asyncio.sleep(0.1)
        print('------\nsearching results\n------')
        driver.get(r"https://search.mcmod.cn/s?key="+ asking)
        await asyncio.sleep(0.1)
        print('------------taking screenshot------------')
        a = driver.find_elements('class name','result-item')
        
        url = ''
        flag = 0	#用于判断是否成功截图	
        # mod_answer = ''
        other = []
        # others = []
        if len(a)>0:#找第一个搜索结果
            other = a[1:5]
            # others = [x.find_element('partial link text','mcmod').text for x in other]
            flag = 1
            b = a[0]
            c = b.find_element('partial link text','mcmod')
            url = c.text
            if not url.startswith('https://'):
                url = "https://" + url
            await asyncio.sleep(0.1)
            driver.get(url)
            async with async_playwright() as playwright:
                logging.info('------init options------')
                webkit = playwright.webkit # or "firefox" or "webkit".
                browser = await webkit.launch()
                page = await browser.new_page()
                logging.info('------searching results------')
                await page.goto(url)
                await page.screenshot(path=os.path.join(PIC,f'{event.author["id"]}_mcmod.jpg'),full_page=True,type='jpeg',quality=25)
                await browser.close()
                logging.info('everything done')

        driver.close()
        driver.quit()
        print('------\nsearching done\n------')
        if flag == 1:
            logging.info(f'{load_config("./imgserver.cfg")["host:port_for_tencent"]}img/{event.author["id"]}_mcmod.jpg')
            await api.send_img(event,f'{load_config("./imgserver.cfg")["host:port_for_tencent"]}img/{event.author["id"]}_mcmod.jpg')
        else:
            await api.send(event,'查询出错，页面不存在或已被删除。')

