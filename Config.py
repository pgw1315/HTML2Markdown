# 默认下载目录
markdown_dir = "/Users/will/Blog/pgw1315.github.io/source/_posts"

webdriver_path = r"/Users/will/PycharmProjects/HTML2Markdown/chromedriver"
# markdown_dir = "markdown"
# img_dir = "markdown/img"
# 图片配置
config_img_download = True

# 使用原来图片的站点
config_use_original_image_domain = ["jianshu.com"]
config_img_dir = "/Users/will/Blog/pgw1315.github.io/source/images"
# Hexo主题的头信息
hexo_head_enable = True
hexo_head = """---
title: {title}
date: {date_time}
author: Will
img: /images/banner/default.jpeg
categories: {categories}
tags:
  - Python
---
        """
# 参考文章
refer_article_enable = True
# 文章是否保存
page_save = True
# 如果文章存在是否覆盖
page_rewrite = False

img_src_list = ["src", "data-original-src", "data-src"]
sites_adapters = [
    # 适配cnblogs
    {
        "domain": "cnblogs.com",
        "title_tag": "a",
        "title_attrs": {"id": "cb_post_title_url"},
        "content_tag": "div",
        "content_attrs": {'id': 'cnblogs_post_body'}
    },

    {
        # 适配CSDN
        "domain": "csdn.net",
        "title_tag": "h1",
        "title_attrs": {'class': 'title-article'},
        "content_tag": "div",
        "content_attrs": {'id': 'content_views'},
    },
    {
        # 适配简书
        "domain": "jianshu.com",
        "title_tag": "h1",
        "title_attrs": {'class': '_1RuRku'},
        "content_tag": "article",
        "content_attrs": {'class': '_2rhmJa'},
    },
    {
        # 程序员客栈
        "domain": "proginn.com",
        "title_tag": "h1",
        "title_attrs": {'id': 'topic_title'},
        "content_tag": "div",
        "content_attrs": {'class': 'rich_media_content'},
    }, {
        # 掘金
        "domain": "juejin.cn",
        "title_tag": "h1",
        "title_attrs": {'class': 'article-title'},
        "content_tag": "div",
        "content_attrs": {'class': 'article-content'},

    }, {
        #
        "domain": "segmentfault",
        "title_tag": "title",
        "title_attrs": {},
        "content_tag": "article",
        "content_attrs": {'class': 'article'},

    }, {
        #
        "domain": "zhihu.com",
        "title_tag": "h1",
        "title_attrs": {'class': "Post-Title"},
        "content_tag": "div",
        "content_attrs": {'class': 'Post-RichTextContainer'},

    }, {
        #
        "domain": "itpub.net",
        "title_tag": "div",
        "title_attrs": {'class': "tit"},
        "content_tag": "div",
        "content_attrs": {'class': 'content'},

    }, {
        #
        "domain": "weixin.qq.com",
        "title_tag": "h1",
        "title_attrs": {'class': "rich_media_title"},
        "content_tag": "div",
        "content_attrs": {'class': 'rich_media_content'},

    }, {
        #
        "domain": "cloud.tencent.com",
        "title_tag": "h1",
        "title_attrs": {'class': "article-title"},
        "content_tag": "div",
        "content_attrs": {'class': 'J-articleContent'},

    }, {
        #
        "domain": "ipcpu.com",
        "title_tag": "h1",
        "title_attrs": {'class': "article-title"},
        "content_tag": "article",
        "content_attrs": {'class': 'article-content'},

    },

]
