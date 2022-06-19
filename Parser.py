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
import datetime
import os
import time
from os.path import exists
from urllib.parse import urljoin

import httpx
import requests
from bs4 import BeautifulSoup, Tag, NavigableString, Comment

from Config import img_src_list, config_img_download, config_img_dir
from Utils import download_img


class Parser(object):
    def __init__(self, html, title):
        self.special_characters = {
            "&lt;": "<", "&gt;": ">", "&nbsp;": " ", "&nbsp": " ",
            "&#8203": "",
        }
        self.html = html
        # 不解析的标签
        self.ignore_tags = ['title', 'style', 'script']

        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.outputs = []

        self.equ_inline = False
        self.title = title
        self.page_img_dir = config_img_dir+"/"+title
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
            self.on_headle_elements(soup)
        # 判断是否还有子节点，如果没有直接退出
        if not hasattr(soup, 'children'):
            return
        # 如果有子节点则遍历
        for child in soup.children:
            self.recursive(child)

    # 处理HTML元素的解析
    def on_headle_elements(self, soup):
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
            soup.contents.insert(0, NavigableString('\n```bash\n'))
            soup.contents.append(NavigableString('\n```\n'))
        elif tag in ['code', 'tt']:
            # 判断code标签是否放在pre标签里面
            if soup.parent.name != "pre":
                soup.contents.insert(0, NavigableString('`'))
                soup.contents.append(NavigableString('`'))
        elif tag == 'p':
            if soup.parent.name != 'li':
                soup.contents.insert(0, NavigableString('\n'))
        elif tag == 'span':

            pass
        elif tag in ['ol', 'ul']:
            soup.contents.insert(0, NavigableString('\n'))
            soup.contents.append(NavigableString('\n'))
        elif tag in ['li']:
            soup.contents.insert(0, NavigableString('\n+ '))
        elif tag == 'tbody':
            self.remove_empty_lines(soup)
            self.remove_empty_lines(soup.contents[0])
            # 获取到第一行
            td = soup.contents[0].contents
            column_count = td.__len__()
            # 生成markdown表头
            mthead = "\n| "
            for column in range(int(column_count)):
                mthead += "--- |"
            mthead += '\n'
            soup.contents.insert(1, NavigableString('%s' % mthead))

            pass
        elif tag == 'tr':
            self.remove_empty_lines(soup)
            soup.contents.append(NavigableString("|\n"))
            pass
        elif tag == 'td':
            soup.contents.insert(0, NavigableString(' | '))
            pass
        elif tag == 'img':
            code = self.process_img(soup)
            self.outputs.append('\n' + code)
        elif tag == 'br':
            soup.contents.insert(0, NavigableString('\n+ '))
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
        for img_src in img_src_list:
            img_url = soup.attrs.get(img_src, '')
            if img_url.startswith("http") or img_url.startswith("/"):
                break
        # 找不到图片
        if not img_url:
            return code
        # 不下载图片，引用原图片
        if not config_img_download:
            code = '![{}]({})'.format(alt, img_url)
            return code

        # 下载图片
        img_url = urljoin("https://", img_url)
        file_name = download_img(img_url, self.page_img_dir)
        code = '![{}]({})'.format(alt, "/images/" +
                                  self.title + "/" + file_name)
        return code


if __name__ == '__main__':
    # html = '<body><!-- cde --><h1>This is 1 &lt;= 2<!-- abc --> <b>title</b></h1><p><a href="www.hello.com">hello</a></p><b>test</b>'
    html = """ 
     <table>
        <tbody>
            <tr>
                <td>命令</td>
                <td>功能说明</td>
                <td>功能说明</td>
                <td>功能说明</td>
                <td>功能说明</td>
            </tr>
            
            
            
            <tr>
                <td>CD</td>
                <td>切换目录</td>
                <td>切换目录</td>
                <td>切换目录</td>
                <td>切换目录</td>
            </tr>
            <tr>
                <td>CD</td>
                <td>切换目录</td>
                <td>切换目录</td>
                <td>切换目录</td>
                <td>切换目录</td>
            </tr>
            
            
            
            
            <tr>
                <td>CD</td>
                <td>切换目录</td>
                <td>切换目录</td>
                <td>切换目录</td>
                <td>切换目录</td>
            </tr>
            <tr>
                <td>CD</td>
                <td>切换目录</td>
                <td>切换目录</td>
                <td>切换目录</td>
                <td>切换目录</td>
            </tr>
        </tbody>
     </table>
     
     """
    parser = Parser(html, '')
    print(''.join(parser.outputs))
