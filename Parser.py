# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@项目 :  HTML2Markdown
@文件 :  Parser.py
@时间 :  2022/06/11 14:14
@作者 :  will
@版本 :  1.0
@说明 :  解析HTML

'''
import os
import platform
from os.path import exists
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup, Tag, NavigableString, Comment

from Utils import download_img, yaml_config_load

current_work_dir = os.path.dirname(__file__)  # 当前文件所在的目录


class Parser(object):
    def init_config(self):
        config_path = os.path.join(current_work_dir, 'config.yaml')
        self.cfg = yaml_config_load(config_path).get('config')
        # 判断是否为hexo文章
        self.hexo_enable = self.cfg['hexo_enable']
        if self.hexo_enable:
            # Hexo博客文章
            self.img_dir = self.cfg['hexo']['img_dir']
        else:
            # 普通Markdown
            self.img_dir = self.cfg['markdown']['img_dir']
        # 图片src属性适配
        self.img_src_list = self.cfg['image']['src_list']
        self.config_img_download = self.cfg['image']['download']
        pass

    def __init__(self, html, title, url=''):

        self.html = html
        self.title = title
        self.url = url

        self.init_config()
        self.special_characters = {
            "&lt;": "<", "&gt;": ">", "&nbsp;": " ", "&nbsp": " ",
            "&#8203": "",
        }
        # 不解析的标签
        self.ignore_tags = ['title', 'style', 'script', 'nav']

        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.outputs = []
        self.equ_inline = False
        self.handler = HandlerFactory.getHandler(url)

        os_name = platform.system()
        if os_name == "Windows":
            # 文件名不能包含以下字符：< > : " / \ | ? *。
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                title = title.replace(char, "-")
        title = title.replace('\n', '')
        title = title.replace('\t\n', '')
        self.page_img_dir = self.img_dir + "/" + title
        if not exists(self.page_img_dir):
            os.makedirs(self.page_img_dir)
        pass
        self.recursive(self.soup)

    def remove_comment(self, soup):
        if not hasattr(soup, 'children'):
            return
        for c in soup.children:
            if isinstance(c, Comment):
                c.extract()
            self.remove_comment(c)

    def recursive(self, soup):
        # 判断是否是注释或者特殊字符
        if isinstance(soup, Comment):
            return
        # 处理字符节点内容
        elif isinstance(soup, NavigableString):
            # 如果是忽略的标签直接跳过
            if soup.parent and soup.parent.name in self.ignore_tags:
                return
            for key, val in self.special_characters.items():
                soup.string = soup.string.replace(key, val)
            self.outputs.append(soup.string)
        # 处理元素节点
        elif isinstance(soup, Tag):
            # 如果是忽略的标签直接跳过
            if soup.name in self.ignore_tags:
                return
            self.on_handle_elements(soup)
        # 判断是否还有子节点，如果没有直接退出
        if not hasattr(soup, 'children'):
            return
        # 如果有子节点则遍历
        for child in soup.children:
            self.recursive(child)

    # 处理HTML元素的解析
    def on_handle_elements(self, soup):
        tag = soup.name
        # 如果是忽略的标签直接跳过
        if tag in self.ignore_tags:
            return
        elif tag in ['h1', 'h2', 'h3', 'h4', 'h5']:
            n = int(tag[1])
            soup.contents.insert(0, NavigableString('\n' + '#' * n + ' '))
            soup.contents.append(NavigableString('\n'))
        elif tag == 'a' and 'href' in soup.attrs:
            soup.contents.insert(0, NavigableString('['))
            soup.contents.append(NavigableString(
                "]({})".format(soup.attrs['href'])))
        elif tag in ['b', 'strong']:
            soup.contents.insert(0, NavigableString('**'))
            soup.contents.append(NavigableString('**'))
        elif tag in ['em']:
            soup.contents.insert(0, NavigableString('*'))
            soup.contents.append(NavigableString('*'))
        elif tag == 'pre':
            self.handler.handle_pre(soup)

        elif tag in ['code', 'tt']:
            self.handler.handle_code(soup)
        elif tag == 'p':
            if soup.parent.name != 'li':
                soup.contents.insert(0, NavigableString('\n'))
        elif tag == 'span':

            pass
        elif tag in ['ol', 'ul']:
            self.handler.handle_ol(soup)
        elif tag in ['li']:
            self.handler.handle_li(soup)
        elif tag == 'tbody':
            self.remove_empty_lines(soup)
            self.remove_empty_lines(soup.contents[0])
            # 获取到第一行
            td = soup.contents[0].contents
            column_count = td.__len__()
            # 生成markdown表头
            mthead = "| "
            for column in range(int(column_count)):
                mthead += "--- |"
            mthead += '\n'
            soup.contents.insert(0, NavigableString('%s' % mthead))
            pass
        elif tag == 'tr':
            self.remove_empty_lines(soup)
            soup.contents.append(NavigableString("|\n"))
            pass
        elif tag == 'th':
            self.remove_empty_lines(soup)
            soup.contents.insert(0, NavigableString(' | '))
            pass
        elif tag == 'td':
            soup.contents.insert(0, NavigableString(' | '))
            pass
        elif tag == 'img':
            code = self.process_img(soup)
            self.outputs.append('\n' + code)
        elif tag == 'blockquote':
            soup.contents.insert(0, NavigableString('> '))
            soup.contents.append(NavigableString('\n'))
        elif tag == 'br':
            soup.contents.insert(0, NavigableString('\n'))
        else:
            pass
        pass

    def remove_empty_lines(self, soup):
        for content in soup.contents:
            if content == "\n":
                soup.contents.remove(content)
        pass

    def process_img(self, soup):
        alt = soup.attrs.get('alt', '')
        img_url = ''
        code = ""
        for img_src in self.img_src_list:
            img_url = soup.attrs.get(img_src, '')
            if img_url.startswith("http") or img_url.startswith("/"):
                break
        # 找不到图片
        if not img_url:
            return code

        # 下载图片
        o = urlparse(self.url)
        host = o.scheme + "://" + o.hostname
        img_url = urljoin(host, img_url)

        # 不下载图片，引用原图片
        if not self.config_img_download:
            code = '![{}]({})'.format(alt, img_url)
            return code

        file_name = download_img(img_url, self.page_img_dir)
        code = '![{}]({})'.format(alt, "/images/" +
                                  self.title + "/" + file_name)
        return code


class HandlerFactory(object):
    @staticmethod
    def getHandler(url):
        if 'csdn.net' in url:
            return CSDNHandler()
        else:
            return Handler()

class Handler(object):
    def handle_pre(self, soup):
        # 语言
        language = self.extract_language(soup)
        if language is None:
            soup.contents.insert(0, NavigableString('\n```\n'))
        else:
            soup.contents.insert(0, NavigableString('\n```' + language + '\n'))
        soup.contents.append(NavigableString('\n```\n'))

    def handle_code(self,soup):
        # 判断code标签是否放在pre标签里面
        if soup.parent.name != "pre":
            soup.contents.insert(0, NavigableString('`'))
            soup.contents.append(NavigableString('`'))

    def handle_ol(self, soup):
        soup.contents.insert(0, NavigableString('\n'))
        soup.contents.append(NavigableString('\n'))

    def handle_li(self, soup):
        parent = soup.parent
        depth = -1
        print(parent.name)
        # 嵌套的列表项正确的缩进
        while parent.name in ['ol', 'ul', 'li']:
            if parent.name in ['ol', 'ul']:
                depth = depth + 1
            parent = parent.parent
        indent = '\t' * depth
        soup.contents.insert(0, NavigableString('\n' + indent + '+ '))

    def extract_language(self, soup):
        """ 输入pre code span，分析其中有没有class标记了语言块 """
        clazz = soup.get("class")
        if clazz is not None:
            if 'language-sql' in clazz:
                return 'sql'
            elif 'language-java' in clazz:
                return 'java'
            elif 'language-cpp' in clazz:
                return 'cpp'
        child = soup.find('code')
        if child is None:
            return None
        return self.extract_language(child)


class CSDNHandler(Handler):
    def handle_pre(self, soup):
        # 语言
        language = self.extract_language(soup)
        if language is None:
            soup.contents.insert(0, NavigableString('\n```\n'))
        else:
            soup.contents.insert(0, NavigableString('\n```' + language + '\n'))
        soup.contents.append(NavigableString('```\n')) # 少一个换行
