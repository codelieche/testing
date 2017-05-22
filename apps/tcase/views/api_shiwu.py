# -*- coding:utf-8 -*-
"""
这个是事务相关的api
"""
import os
import json

from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse, HttpResponse, Http404
from django.template import loader, Context
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.conf import settings
import requests

from utils.mixins import LoginRequiredMixin, CsrfExemptMixin
from utils.shiwu_handle import shiwu_str_to_json, shiwu_str_to_list
from utils.make_check_shiwu_code import make_check_shiwu_code
from ..models import Shiwu
from ..forms import ShiwuForm


class ShiwuAddApiView(LoginRequiredMixin, View):
    """
    添加事务的api
    """
    def post(self, request):
        # 权限判断：需要tcase.add_case的权限
        # 有了add_case的权限，也就有了add_shiwu的权限
        if not request.user.has_perm('tcase.add_case'):
            raise PermissionDenied

        # 先获取post过来的数据
        shiwu_form = ShiwuForm(request.POST)
        if shiwu_form.is_valid():
            shiwu = shiwu_form.save()
            # 保存user id
            shiwu.user_id = request.user.id
            # 保存 请求事务数据
            types = request.POST.getlist('type')
            keys = request.POST.getlist('key')
            values = request.POST.getlist('value')
            body = shiwu_str_to_json(types, keys, values)
            # for i in range(len(keys)):
            #     if keys[i] and values[i]:
            #         body[keys[i]] = values[i]
            shiwu.body = body
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
        # edit的页面，只给ajax访问
        if not request.is_ajax():
            raise Http404
        # 先获取到事务
        shiwu = get_object_or_404(Shiwu, pk=pk)
        # 渲染内容
        all_method = Shiwu.METHOD_CHOICES
        # key_value的类型：
        types = (
            ('one', "单值"),
            ('many', "多值"),
            ('list', "列表")
        )
        # 处理请求事务的body信息
        body = shiwu_str_to_list(shiwu.body)
        c = {
            'shiwu': shiwu,
            'all_method': all_method,
            'types': types,
            'body': body
        }
        # 渲染内容
        html = render_to_string('case/edit_shiwu.html', c, request=request)
        return HttpResponse(html)

    def post(self, request, pk):
        # 先获取到事务
        shiwu = get_object_or_404(Shiwu, pk=pk)
        form = ShiwuForm(request.POST, instance=shiwu)
        # 是否通过验证
        if form.is_valid():
            shiwu = form.save()

            # 请求事务body数据：转成json然后保存其字符串
            types = request.POST.getlist('type')
            keys = request.POST.getlist('key')
            values = request.POST.getlist('value')
            body = shiwu_str_to_json(types, keys, values)
            shiwu.body = json.dumps(body)
            shiwu.save()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "msg": str(form.errors)})


class ShiwuCheckApiView(CsrfExemptMixin, View):
    """
    验证请求事务的API
    """
    def post(self, request):
        # 需要传递事务的shiwu_id, case_id, cookies
        # 而且只有编辑事务的时候，才有验证的功能

        shiwu_id = request.POST.get('shiwu_id', 0)
        shiwu = get_object_or_404(Shiwu, pk=shiwu_id)
        # start_shiwu
        if shiwu.is_startup:
            start_shiwu = None
        else:
            start_shiwu = Shiwu.objects.filter(project=shiwu.project,
                                               is_startup=True).first()
        cookies = request.POST.get('cookies', '')
        base_dir_parent = os.path.dirname(settings.BASE_DIR)
        script_dir = os.path.join(base_dir_parent, 'scripts')
        check_file_name = 'shiwu_{}_check.py'.format(shiwu_id)
        file_path = os.path.join(script_dir, check_file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            file_code = make_check_shiwu_code(shiwu, start_shiwu, cookies)
            f.write(file_code)
        # 执行代码
        p = os.popen('python %s' % file_path)
        content = p.read()
        # print(content)
        return HttpResponse(content)
