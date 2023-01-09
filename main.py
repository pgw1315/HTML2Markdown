# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
@项目 :  PD
@文件 :  mian.py
@时间 :  2022/06/11 14:14
@作者 :  will
@版本 :  1.0
@说明 :  下载网页

'''

import httpx
from bs4 import BeautifulSoup
import ssl

from HTML2Markdown.WordPress import WordPress

ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://zhuanlan.zhihu.com/p/35973068?utm_id=0'
content = httpx.get(url).content
soup = BeautifulSoup(content, 'html.parser', from_encoding="utf-8")
title = soup.find('h1', {'class': "Post-Title"}).text
content = soup.find('div', {'class': "Post-RichTextContainer"})

url='https://vv.iwjing.fun/xmlrpc.php'
user='xiaogang'
pwd='wei@1992.'
wp=WordPress(url,user,pwd)

# 剔除样式标签
styles = content.findAll('style')
for style in styles:
    style.decompose()
# 剔除脚本标签
jss = content.findAll('script')
for js in jss:
    js.decompose()
# 处理图片问题
imgs = content.findAll('img')
# try:
for img in imgs:
    # 将图片上传到自己的WordPress
    # img_src=img.attrs['data-original']
    # file='./'+os.path.basename(img_src)
    # wget.download(img_src,file)
    # img.attrs['src'] =  wp.upload_img(file)
    img.attrs['src'] = img.attrs['data-actualsrc']
# except:
#     pass

content = str(content)

p=wp.post(title,content)
# p=wp.upload_img('./img.jpg')
print(p)
