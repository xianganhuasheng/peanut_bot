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
            await asyncio.sleep(0.1)
            k = 1
            js_height = "return document.body.clientHeight"
            height = driver.execute_script(js_height)
            while k * 500 < height:
                js_move = "window.scrollTo(0,{})".format(k * 500)
                print(js_move)
                driver.execute_script(js_move)
                await asyncio.sleep(0.5)
                height = driver.execute_script(js_height)
                comment_box_y = driver.find_elements('class name','comment-title')
                print(comment_box_y)
                if len(comment_box_y)>0:
                    height = comment_box_y[0].location.get('y')
                k += 1
            #设置浏览器长宽到最大范围方便截图
            w = driver.execute_script("return document.documentElement.scrollWidth")
            h = driver.execute_script("return document.documentElement.scrollHeight")
            driver.set_window_size(w,h)
            url = driver.current_url
            driver.implicitly_wait(5)
            await asyncio.sleep(0.1)
            print('------\nsaving screenshot\n------')
            print(os.path.join(PIC,f'{event.author["id"]}_mcmod.jpg'))
            try:
                b64_img:str = driver.get_screenshot_as_base64()
                binary_img = base64.b64decode(b64_img)
                img = Image.open(BytesIO(binary_img))
                img = img.convert("RGB")
                img.save(os.path.join(PIC,f'{event.author["id"]}_mcmod.jpg'))
            except Exception as e:
                logging.error(e)
        driver.close()
        driver.quit()
        print('------\nsearching done\n------')
        if flag == 1:
            print(f'{load_config("./imgserver.cfg")["host:port_for_tencent"]}img/{event.author["id"]}_mcmod.jpg')
            await api.send_img(event,f'{load_config("./imgserver.cfg")["host:port_for_tencent"]}img/{event.author["id"]}_mcmod.jpg')
        else:
            await api.send(event,'查询出错，页面不存在或已被删除。')
