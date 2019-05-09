# -*- coding:utf-8 -*-
from __future__ import absolute_import

import os
import django

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webpts.settings')
# django.setup()

# 可以在实例化Celery的时候传入broker、backend参数。也可以在settings中配置BROKER_URL
app = Celery('webpts')
'''
BROKER_URL = 'redis://127.0.0.1:6379/0'
BACKEND_URL = 'redis://127.0.0.1:6379/1'

app = Celery('webpts', broker=BROKER_URL, backend=BACKEND_URL)
'''

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
