'''
Author: will
Date: 2022-06-12 04:30:33
LastEditTime: 2022-06-19 12:23:52
FilePath: /HTML2Markdown/Utils.py
Description: 

'''
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
def download_img(url, img_dir='.', file_path=None):
    """
    下载图片到本地
    :param url:
    :param img_dir:
    :param file_path:
    :return:下载后的文件名
    """
    response = httpx.get(url)
    path = ""
    if response.status_code == 200:
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
    l = yaml_config_load('config.yaml')
    print(l.get('md_dir'))
