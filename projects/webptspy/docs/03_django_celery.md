## Celery与Django的结合：简单使用

- 创建了项目webpts
- 创建了app tresult

### 新建celery.py文件
> wepbts/celery.py

```python
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

app = Celery('webpts',broker=BROKER_URL,backend=BACKEND_URL,)
'''

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

``` 

### 编辑webpts/__init__.py

```python
# -*- coding:utf-8 -*-
from __future__ import absolute_import

from .celery import app as celery_app

__all__ = ['celery_app']

```

### 创建tasks.py文件
> tresult/tasks.py

```python
# -*- coding:utf-8 -*-
from celery import shared_task

@shared_task
def hello():
    print('Hello Celery')
    from time import sleep
    sleep(3)
    print('sleep 3 ok!')
    print('Hello hahahha')
    return 'hello return str'
```


### 在view中异步调用任务
> tresult/views.py

```python
from tresult.tasks import hello

# 在需要调用hello任务的地方使用
hello.delay()
```

### 启用Celery
- 启动命令：`celery -A webpts worker -l info`

## 注意事项
- 这里本地需要启动redis服务
- 启动django项目的同时需要启动celery任务