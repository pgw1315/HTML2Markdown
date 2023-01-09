'''
Author: will
Date: 2022-06-12 04:30:33
LastEditTime: 2022-06-19 12:23:52
FilePath: /HTML2Markdown/Utils.py
Description:

'''
import os

# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  HTML2Markdown
@文件 :  Utils.py
@时间 :  2022/06/12 04:30
@作者 :  will
@版本 :  1.0
@说明 :   工具类

'''




import time
from urllib.parse import urlparse
import httpx
import yaml


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

current_work_dir = os.path.dirname(__file__)  # 当前文件所在的目录
def broser_load( url):
    # 使用浏览器加载页面
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    # 禁止沙箱模式，否则肯能会报错遇到chrome异常
    chrome_options.add_argument('--no-sandbox')
    brower = webdriver.Chrome(service=Service(os.path.join(current_work_dir, 'chromedriver')),
                              options=chrome_options)
    brower.get(url)
    brower.implicitly_wait(10)
    content = brower.page_source
    brower.quit()
    return content

def download_img(url, img_dir='.', file_path=None):
    """
    下载图片到本地
    :param url:
    :param img_dir:
    :param file_path:
    :return:下载后的文件名,如果下载失败则返回空字符串
    """
    try:
        response = httpx.get(url)
        path = ""
        # 如果返回302自动跳转
        if response.status_code == 302:
            l = response.headers.get('location')
            if l:
                return download_img(l, img_dir, file_path)
            pass
        elif response.status_code == 200:
            # 判断是否有传入的文件名，如果没有，则使用当前的时间戳生成一个文件名
            file_type = response.headers.get("content-type").split('/')[1]
            if not file_path:
                # 如果能获取到文件名则获取文件名，如果获取不到则使用时间戳
                up = urlparse(url)
                file_name = up.path.split('/')[-1:]
                if file_name:
                    file_name = file_name[0]
                else:
                    file_name = str(int(time.time()))
                n_name = file_name.split('.')[:-1]
                if n_name:
                    file_name = '.'.join(n_name)

                file_path = img_dir + '/' + file_name + '.' + file_type
                path = file_name + '.' + file_type
            else:
                file_path = file_path + '.' + file_type
                path = file_path
            try:
                f = open(file_path, 'wb')
                f.write(response.content)
                f.close()
            except Exception as e:
                pass

        return path
    except:
        return ''


def yaml_config_load(path):
    """
    加载yaml项目配置文件
    """
    config_list = []
    with open(path, 'rb') as f:
        # yaml文件通过---分节，多个节组合成一个列表
        config = yaml.safe_load_all(f)
        config_list = list(config)
        pass
    return dict(config_list[0])


def format_special_characters(str, separator='_'):
    """
    格式化特殊字符
    """
    if not str:
        return ''

    special_chars = ['*', '?', '\\', '/', '<', '>', ':', '"']
    for schar in special_chars:
        str = str.replace(schar, separator)
    return str


if __name__ == '__main__':
    url = 'https://segmentfault.com/img/remote/1460000021654930'
    download_img(url)
