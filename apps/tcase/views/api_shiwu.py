# -*- coding:utf-8 -*-
"""
这个是事务相关的api
"""
import json

from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.template import loader, Context

from utils.mixins import LoginRequiredMixin

from ..models import Shiwu
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
                if keys[i] and values[i]:
                    body[keys[i]] = values[i]
            shiwu.body = json.dumps(body)
            shiwu.save()
            # 渲染li html
            t = loader.get_template('case/shiwu_li.html')
            # 渲染内容
            c = Context({'shiwu': shiwu})
            # 渲染html
            html = t.render(c)
            return HttpResponse(html)
        else:
            return JsonResponse({"status": "failure",
                                 "msg": str(shiwu_form.errors)},
                                status=400)


class ShiwuEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # 先获取到事务
        shiwu = get_object_or_404(Shiwu, pk=pk)
        # 获取loader html
        t = loader.get_template('case/edit_shiwu.html')
        # 渲染内容
        all_method = Shiwu.METHOD_CHOICES
        # 处理请求事务的body信息
        body = json.loads(shiwu.body)

        c = Context({
            'shiwu': shiwu,
            'all_method': all_method,
            'body': body
        })
        # 渲染html
        html = t.render(c)
        return HttpResponse(html)
