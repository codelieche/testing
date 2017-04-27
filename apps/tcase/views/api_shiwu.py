# -*- coding:utf-8 -*-
"""
这个是事务相关的api
"""
import json

from django.views.generic import View
from django.http import JsonResponse

from utils.mixins import LoginRequiredMixin

from ..forms import ShiwuForm


class ShiwuAddApiView(LoginRequiredMixin, View):
    """
    添加事务的api
    """
    def post(self, request):
        # 先获取post过来的数据
        shiwu_form = ShiwuForm(request.POST)
        if shiwu_form.is_valid():
            shiwu = shiwu_form.save()
            # 保存user id
            shiwu.user_id = request.user.id
            # 保存 请求事务数据
            keys = request.POST.getlist('key')
            values = request.POST.getlist('value')
            body = {}
            for i in range(len(keys)):
                body[keys[i]] = values[i]
            shiwu.body = json.dumps(body)
            shiwu.save()
            return JsonResponse({'status': "success", "msg": "OK"})
        else:
            return JsonResponse({"status": "failure",
                                 "msg": str(shiwu_form.errors)})
