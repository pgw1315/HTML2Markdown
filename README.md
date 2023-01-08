# HTML2Markdown

HTML2Markdown工具为将网页导出为Markdown文件，目前支持CSDN，知乎等文章直接导出，并生成支持Hexo博客的文章。

### 目前支持导出的网站
 
+ [cnblogs.com](cnblogs.com)
+ [csdn.net](csdn.net)
+ [jianshu.com](jianshu.com)
+ [proginn.com](proginn.com)
+ [juejin.cn](juejin.cn)
+ [segmentfault.com](segmentfault.com)
+ [zhihu.com](zhihu.com)
+ [itpub.net](itpub.net)
+ [weixin.qq.com](weixin.qq.com)

### 环境配置
安装python3

```shell
#安装epel
 wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
 #安装python36
 yum install python36 -y
 #安装pip3
 yum install python36-pip -y
 #安装python开发工具
 yum install python36-devel -y

```


### 安装必要的扩展包

```shell
pip3 install httpx
pip3 install requests
pip3 install pyyaml
pip3 install selenium
pip3 install beautifulsoup4
```

### 使用方法

```shell
 python3 PageDown.py
```


