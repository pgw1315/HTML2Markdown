# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
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

import httpx
from bs4 import BeautifulSoup

from Config import sites_adapters, markdown_dir, hexo_head, hexo_head_enable, refer_article_enable, page_save, \
    page_rewrite, webdriver_path, config_img_dir
from Parser import Parser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class PageDown():

    def __init__(self):

        # 使用浏览器加载页面
        self.browser_to_load_domains = ["juejin.cn"]
        # 如果目录不存在创建目录
        if not exists(markdown_dir):
            os.makedirs(markdown_dir)
        pass



    def download_page(self, url):

        # 加载内容
        content = self.on_load_page(url)
        soup = BeautifulSoup(content, 'html.parser', from_encoding="utf-8")
        # 解析之前调用
        content = self.on_parse_before(content)
        # 解析标题和内容
        title, content = self.on_parse_title_content(soup, url)

        if not exists(config_img_dir):
            os.makedirs(config_img_dir)
        pass
        # 解析HTML转换为MarkDown
        parser = Parser(content, title)
        content = ''.join(parser.outputs)
        # 解析完成
        content = self.on_parse_complete(url, title, content)
        # 保存
        if page_save:
            self.save(title, content)

    def on_parse_title_content(self, soup, url):
        is_adapter = False
        title = ""
        html = ''
        for sites_adapter in sites_adapters:
            if sites_adapter['domain'] in url:
                is_adapter = True
                # 获取标题
                title_tag = soup.find(sites_adapter['title_tag'], sites_adapter['title_attrs'])
                if title_tag:
                    title = title_tag.text
                else:
                    title = soup.title.text
                # 获取内容
                for c in soup.find_all(sites_adapter['content_tag'], sites_adapter['content_attrs']):
                    html += str(c)

        # 没有适配
        if not is_adapter:
            title = soup.title.text
            html = soup.find("body")
        # 替换特殊字符
        title = '_'.join(title.replace('*', '').strip().split())
        return title, html;
        pass

    def on_parse_before(self, content):

        return content

    def on_parse_complete(self, url, title, content):
        # 替换多余的空格
        content = content.replace(r"\s{2,}", "")

        # 添加头信息
        if hexo_head_enable:
            x = datetime.datetime.now()
            date_time = x.strftime("%Y-%m-%d %H:%M:%S")
            head_format = hexo_head.format(title=title, date_time=date_time, categories="")
            content = head_format + content

        # 添加参考文章
        if refer_article_enable:
            foot = "\n\n## 参考文章\n[{}]({})".format(title, url)
            content = content + foot
        return content

    def save(self, title, content):
        # MarkDown文件名
        md_file = markdown_dir + "/" + title + '.md'
        if exists(md_file) and not page_rewrite:
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

    def on_load_page(self, url):
        browser = False
        for browser_to_load_domain in self.browser_to_load_domains:
            if browser_to_load_domain in url:
                browser = True
                break
        if browser:
            # 使用浏览器加载页面
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')  # 禁止沙箱模式，否则肯能会报错遇到chrome异常
            brower = webdriver.Chrome(service=Service(webdriver_path),
                                      options=chrome_options)
            brower.get(url)
            brower.implicitly_wait(10)
            content = brower.page_source
            brower.quit()
        else:
            content = httpx.get(url).content
        return content
        pass


if __name__ == '__main__':
    # 内容所在元素

    page_url = input("请输入文章地址：")
    if not page_url:
        print("文章地址不能为空!!")
        exit()
    pd = PageDown()
    pd.download_page(page_url)
