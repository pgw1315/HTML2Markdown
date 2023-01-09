# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
@项目 :  HTML2Markdown
@文件 :  PageDown.py
@时间 :  2022/06/11 14:14
@作者 :  will
@版本 :  1.0
@说明 :  下载网页并生成Markdown

'''


import os
import datetime
from os.path import exists
import re
import sys
import httpx
from bs4 import BeautifulSoup
from Parser import Parser
from Utils import format_special_characters, yaml_config_load


current_work_dir = os.path.dirname(__file__)  # 当前文件所在的目录


class PageDown():

    '''
    描述:
    param {*} self
    return {*}
    '''

    def init_config(self):
        # 配置文件路径
        config_path = os.path.join(current_work_dir, 'config.yaml')
        self.cfg = yaml_config_load(config_path)['config']
        # self.webdriver_path = self.cfg.get('webdriver_path')
        # 浏览器驱动路径
        self.webdriver_path = os.path.join(current_work_dir, 'chromedriver')
        # 判断是否为hexo文章
        self.hexo_enable = self.cfg['hexo']['enable']
        if self.hexo_enable:
            # Hexo博客文章
            self.md_dir = self.cfg['hexo']['post_dir']
            self.img_dir = self.cfg['hexo']['img_dir']
            self.hexo_head = self.cfg['hexo']['content']
        else:
            # 普通Markdown
            self.md_dir = self.cfg['md_dir']
            self.img_dir = self.cfg['image']['dir']
            self.hexo_head = ''

        self.page_rewrite = self.cfg['page']['rewrite']
        self.page_save = self.cfg['page']['save']
        self.page_refer = self.cfg['page']['refer']

        self.adapters = self.cfg['adapters']
        # 使用浏览器加载页面
        self.js_load_list = self.cfg['js_load']

    def __init__(self):
        self.init_config()
        # # 如果目录不存在创建目录
        # if not exists(self.md_dir):
        #     os.makedirs(self.md_dir)
        # pass
        # if not exists(self.img_dir):
        #     os.makedirs(self.img_dir)
        # pass

    def download_page(self, url):

        # 加载内容
        content = httpx.get(url).content
        soup = BeautifulSoup(content, 'html.parser', from_encoding="utf-8")
        # 解析之前调用
        content = self.parse_before(content)
        # 解析标题和内容
        title, content = self.parse_title_content(soup, url)
        # 解析HTML转换为MarkDown
        parser = Parser(content, title, url)
        content = ''.join(parser.outputs)
        # 解析完成
        content = self.parse_complete(url, title, content)
        # 保存
        if self.page_save:
            self.save(title, content)

    def parse_title_content(self, soup, url):
        title = ""
        html = ''
        for adapter in self.adapters:
            if adapter['domain'] in url:

                # 尝试获取标题
                try:
                    t_sel = adapter.get('title', '').split(',')
                    # 获取标题
                    title = soup.find(t_sel[0], {t_sel[1]: t_sel[2]}).text

                except:
                    pass
                # 尝试获取内容
                try:

                    c_sel = adapter.get('content', '').split(',')
                    # 获取内容
                    html = soup.find(c_sel[0], {c_sel[1]: c_sel[2]})
                except:
                    pass
                break

        # 没有适配
        title = title if title else soup.title.text
        html = html if html else soup.find("body")

        # 替换标题中的特殊字符特殊字符
        title = format_special_characters(title)
        title = title.replace(' ', '')
        return title, str(html)

    def parse_before(self, content):

        return content

    def parse_complete(self, url, title, content):
        # 替换多余的空格
        content = re.sub('\n{2,}', '\n\n', content)
        # 添加头信息
        if self.hexo_enable:
            x = datetime.datetime.now()
            date_time = x.strftime("%Y-%m-%d %H:%M:%S")
            head_format = self.hexo_head.format(
                title=title, date_time=date_time, categories="")
            content = head_format + content

        # 添加参考文章
        if self.page_refer:
            foot = "\n\n## 参考文章\n[{}]({})".format(title, url)
            content = content + foot
        return content

    def save(self, title, content):
        # MarkDown文件名
        md_file = self.md_dir + "/" + title + '.md'
        if exists(md_file) and not self.page_rewrite:
            print('文章已经存在: {}'.format(md_file))
            return
        print('保存Markdown文件到: {}'.format(md_file))
        try:
            # 保存文件
            with open(md_file, 'w') as f:
                # 写入文件
                f.write(content)
        except Exception as e:
            print("保存文件失败:" + e)
            exit()
        return content






if __name__ == '__main__':
    url = None
    # 从命令行获取参数
    if sys.argv.__len__() > 1:
        cmd_arg = sys.argv[1]
        if cmd_arg and cmd_arg.startswith('http'):
            url = cmd_arg
    # 要求用户输入文章地址
    if not url:
        url = input("请输入文章地址")
        if not url or not url.startswith('http'):
            print("文章地址为或者格式不正确!!")
            exit()
        pass
    # 初始化目录

    pd = PageDown()
    pd.download_page(url)
