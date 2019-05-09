# -*- coding:utf-8 -*-
import os
import time
import random

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class ImageStorage(FileSystemStorage):
    """
    自定义文件储存
    修改文件名字
    """
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化ImageStorage
        super(ImageStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        """
        复写_save方法
        """
        # 文件后缀名
        file_ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名：年/月/日/分秒随机数
        file_name = time.strftime("%Y%m%H%M%S")
        # 加个0-100的随机数字，防止同时上传多个文件的时候重名
        file_name += '_%d' % random.randint(0, 100)
        # 合成文件名
        name = os.path.join(d, file_name + file_ext)
        # 调用父类方法
        return super(ImageStorage, self)._save(name, content)
