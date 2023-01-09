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
        post.post_status = 'publish'  # ����״̬����дĬ���ǲݸ壬private��ʾ˽�ܵģ�draft��ʾ�ݸ壬publish��ʾ����

        post.terms_names = {
            'post_tag': category,  # ����������ǩ��û�����Զ�����
            'category': post_tag  # �����������࣬û�����Զ�����
        }

        post.custom_fields = []  # �Զ����ֶ��б�
        return self.wp.call(posts.NewPost(post))

    def upload_img(self,file_path):

        filename =os.path.basename(file_path)  # �ϴ���ͼƬ�ļ�·��
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
