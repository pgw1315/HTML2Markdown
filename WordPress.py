import os

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.compat import xmlrpc_client

class WordPress():
    def __init__(self, url, user, passwd):
        self.wp = Client('https://vv.iwjing.fun/xmlrpc.php', 'xiaogang', 'wei@1992.')
        pass

    def post(self,title,content,category=[],post_tag=[]):
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = 'publish'  # 文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布

        post.terms_names = {
            'post_tag': category,  # 文章所属标签，没有则自动创建
            'category': post_tag  # 文章所属分类，没有则自动创建
        }

        post.custom_fields = []  # 自定义字段列表
        return self.wp.call(posts.NewPost(post))

    def upload_img(self,file_path):

        filename =os.path.basename(file_path)  # 上传的图片文件路径
        # prepare metadata
        data = {
            'name': filename,
            'type': 'image/jpeg',  # mimetype
        }
        # read the binary file and let the XMLRPC library encode it into base64
        with open(file_path, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())
        response=self.wp.call(media.UploadFile(data))
        return response['link']
