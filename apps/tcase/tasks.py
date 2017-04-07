# -*- coding:utf-8 -*-
"""
Celery异步任务
"""
import os
import subprocess
from time import sleep
from datetime import datetime

import requests
from django.conf import settings
from django.core.urlresolvers import reverse
from celery import shared_task

from .models import Execute


def port_can_use(port):
    """
    判断端口号是否可用
    :param port:
    :return: True, or False
    """
    url = 'http://127.0.0.1:%s' % port
    try:
        r = requests.get(url, timeout=3)
        return False
    except Exception as e:
        print(e)
        return True


@shared_task
def run_execute(execute_id, host,
                locust_path='~/.pyenv/versions/env_locust_3.5.3/bin/locust'):
    """
    运行Case，并记录下信息
    :param execute_id: 测试用例的id，根据id来找到文件
    :param host: case的测试域名
    :param locust_path: locust命令的位置
    :return:
    """
    # 第一步：获取启动locust的端口号
    port = 8080
    port_can_use_flag = port_can_use(port)
    while port_can_use_flag is False:
        sleep(1)
        port += 1
        port_can_use_flag = port_can_use(port)
    # 把port写入execute中
    execute = Execute.objects.get(pk=execute_id)
    if execute.status in ['created', 'ready']:
        # 保存status和port信息
        execute.port = port
        # 开始执行execute
        # 1. 找到脚本目录
        base_dir_parent = os.path.dirname(settings.BASE_DIR)
        scripts_dir = os.path.join(base_dir_parent, 'scripts')
        case_file_path = os.path.join(scripts_dir, 'case_%s.py' % \
                                      execute.case_id)

        cmd = '{} --locustfile={} --port={} --host={}'.format(locust_path,
                                                              case_file_path,
                                                              port, host)
        execute.status = 'running'
        execute.time_start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        execute.save()
        try:
            result = subprocess.getstatusoutput(cmd)
            # 这里会只等待命令的执行
        except Exception as e:
            pass
        finally:
            # 判断execute是否还在运行。停止服务
            pass


@shared_task
def post_locust_start(host, execute_id, locust_count=10, hatch_rate=1):
    """
    触发启动locust的api
    :param host: Django服务的host, request.META['HTTP_HOST']
    :param execute_id: execute的id
    :return:
    """
    sleep(3)
    post_url = 'http://{}{}'.format(host, reverse('api:execute:locust_start'))
    post_data = {
        'execute_id': execute_id,
        'locust_count': locust_count,
        'hatch_rate': hatch_rate
    }
    r = requests.post(post_url, post_data)
    if not r.ok:
        print(r)


@shared_task
def post_locust_stop(host, execute_id):
    """
    触发停止locust的api
    :param host: Django服务的host, request.META['HTTP_HOST']
    :param execute_id: execute的id
    :return:
    """
    post_url = 'http://{}{}'.format(host, reverse('api:execute:locust_stop'))
    post_data = {
        'execute_id': execute_id,
    }
    r = requests.post(post_url, post_data)
    if not r.ok:
        print(r)


@shared_task
def post_locust_user_add(host, execute_id, locust_count=5, hatch_rate=1):
    """
    触发添加并发用户数locust的api
    :param host: Django服务的host, request.META['HTTP_HOST']
    :param execute_id: execute的id
    :param locust_count: 增加的用户数
    :return:
    """
    ok = True
    while ok:
        sleep(10)
        user_add_url = reverse('api:execute:locust_user_add')
        post_url = 'http://{}{}'.format(host, user_add_url)
        post_data = {
            'execute_id': execute_id,
            'locust_count': locust_count,
            'hatch_rate': hatch_rate
        }
        r = requests.post(post_url, post_data)
        ok = r.ok
