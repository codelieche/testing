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
