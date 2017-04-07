# -*- coding:utf-8 -*-
"""
这个文件主要实现：execute执行了命令后，start、add_user、stop locust的api
"""
import requests
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from utils.mixins import CsrfExemptMixin
from tcase.models import Execute


class LocustStart(CsrfExemptMixin, View):
    """
    开始Locust脚本
    """
    def post(self, request):
        """
        :param request:
        :return:
        """
        # 先获取post过来的数据
        locust_count = request.POST.get('locust_count', '10')
        hatch_rate = request.POST.get('hatch_rate', '1')
        execute_id = request.POST.get('execute_id', 0)
        if execute_id:
            # 获取到execute_id:
            execute = get_object_or_404(Execute, pk=execute_id)
            # 获取execute的port
            port = execute.port
            if execute.status == 'running':
                # 开始发送开始命令
                post_url = 'http://127.0.0.1:%s/swarm' % port
                post_data = {
                    'locust_count': locust_count,
                    'hatch_rate': hatch_rate
                }
                # 发送post数据
                r = requests.post(post_url, post_data)
                return JsonResponse(r.json(), status=r.status_code)
        return JsonResponse({'status': 'failure'}, status=400)


class LocustAddUser(CsrfExemptMixin, View):
    """
    增加Locust并发用户数
    """
    def post(self, request):
        # 先获取post过来的数据
        locust_count = request.POST.get('locust_count', '')
        hatch_rate = request.POST.get('hatch_rate', '1')
        execute_id = request.POST.get('execute_id', 0)
        if execute_id and locust_count:
            # 获取到execute_id:
            execute = get_object_or_404(Execute, pk=execute_id)
            # 获取execute的port
            port = execute.port
            if execute.status == 'running':
                # 开始发送开始命令
                post_url = 'http://127.0.0.1:%s/swarm/add' % port
                post_data = {
                    'locust_count': locust_count,
                    'hatch_rate': hatch_rate
                }
                # 发送post数据
                r = requests.post(post_url, post_data)
                return JsonResponse(r.json(), status=r.status_code)
        return JsonResponse({'status': 'failure'}, status=400)


class LocustStop(CsrfExemptMixin, View):
    """
    停止Locust
    """
    def post(self, request):
        # 先获取post过来的数据
        execute_id = request.POST.get('execute_id', 0)
        if execute_id:
            # 获取到execute_id:
            execute = get_object_or_404(Execute, pk=execute_id)
            # 获取execute的port
            port = execute.port
            if execute.status == 'running':
                # 开始发送开始命令
                stop_url = 'http://127.0.0.1:%s/stop' % port
                try:
                    r = requests.get(stop_url)
                    return JsonResponse({'status': 'success'})
                except Exception as e:
                    print(e)
                    return JsonResponse({'status': 'failure'})
        return JsonResponse({'status': 'failure'}, status=400)
