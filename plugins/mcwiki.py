from selenium import webdriver as wd
from selenium.webdriver.edge.options import Options
import os
import time

from api.message import *
from api.util import *

current_dir = os.path.dirname(__file__)
os.chdir(current_dir)
path = 'file:///'+os.getcwd().replace('\\','/')+'/'

def message_main(data):
    user_message = get_message(data)
    user_id = get_user(data)
    if not os.path.exists('../cache/mcwiki'):
        print('making file ../cache/mcwiki')
        os.mkdir('../cache/mcwiki')
    
    if "刷新wiki"==user_message:
        try:
	    # for 循环删除文件夹中的文件
            for i in os.listdir('../cache/mcwiki'):
        # print(i)
                txt_path=os.path.join('../cache/mcwiki',i)
                os.remove(txt_path)
        except Exception as result:
            print("报错3:%s"%result)
        Message('刷新完了哦~').auto(data).send()
        return True
    
    if user_message.startswith("wiki") and not os.path.exists('../cache/mcwiki/{}_is_searching_wiki'.format(user_id)):
        with open('../cache/mcwiki/{}_is_searching_wiki'.format(user_id),'w'):
            pass
        searching_data = user_message[4:]
        Message('正在努力查询',searching_data,'哟~੭ ᐕ)੭*⁾⁾').auto(data).send()

        print('------\ninit options\n------')
        edge_options = Options()
        edge_options.add_argument('headless')
        edge_options.add_argument('--disable-gpu')
        edge_options.add_argument('--no-sandbox')
        edge_options.add_argument('--hide-scrollbars')
        driver = wd.Edge(options = edge_options)#浏览器设置
        
        print('------\nsearching results\n------')
        driver.get(r"https://zh.minecraft.wiki/w/"+searching_data)

        print('------------taking screenshot------------')
        w = driver.execute_script("return document.documentElement.scrollWidth")
        h = driver.execute_script("return document.documentElement.scrollHeight")
        #设置浏览器长宽到最大范围方便截图
        driver.set_window_size(w,h)
        driver.implicitly_wait(5)
        print('------\nsaving screenshot\n------')
        driver.save_screenshot('../cache/mcwiki/mcwiki_result.png')
        driver.close()
        driver.quit()
        print('everything done')
        Message(image('cache/mcwiki/mcwiki_result.png')).auto(data).send()
        #time.sleep(15)
        os.remove('../cache/mcwiki/{}_is_searching_wiki'.format(user_id))

    return True

def info():
    return "mcwiki查询"
