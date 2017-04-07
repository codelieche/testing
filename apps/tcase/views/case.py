# -*- coding:utf-8 -*-
import os
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied

from utils.mixins import CsrfExemptMixin
from utils.make_case_file import make_case_file
from ..models import Case, Execute
# Create your views here.


class CaseListView(View):
    """
    网站首页View
    """
    def get(self, request):
        all_case = Case.objects.all()
        return render(request, 'case/list.html', {
            'all_case': all_case,
        })


class CaseExecuteView(View):
    """
    执行测试用例View
    执行测试用例需要做的事情：
    1、判断在代码根目录下的 ../scripts/是否存在cese_id.py的文件
        1-1：如果存在，跳过
        1-2：如果不存在，则创建文件
    2、判断case是否有execute_id，没有就创建
    3、根据execute_id获取对应的execute的状态，根据状态做不同的处理
        3-1：如果execute.status是running那么就跳转到这个执行
        3-2: 如果execute.status已经是stoped, falure, sucess状态，
            我们就需要重新创建个新的执行
        3-3：更新相关的状态、跳转到新的执行
    """
    def get(self, request, pk):
        # 根据pk获取到对应的case
        case = get_object_or_404(Case, pk=pk)

        # 第一步：先判断case_id.py的文件是否存在
        base_dir_parent = os.path.dirname(settings.BASE_DIR)
        scripts_dir = os.path.join(base_dir_parent, 'scripts')
        case_file_name = 'case_%s.py' % pk
        case_file_path = os.path.join(scripts_dir, case_file_name)
        # 判断文件是否存在
        if not os.path.exists(case_file_path):
            # 如果不存在，就写入文件
            result = make_case_file(
                code_content=case.code,
                file_name=case_file_name,
                case_id=pk
            )
            # 如果result是False就需要抛出500错误

        # 第二步：判断execute_id是否存在, 判断是否要创建新的execute
        need_create_execute = False
        execute = None
        # 判断是否存在execute id
        if case.execute_id:
            # 有execute_id字段 还需要判断这个execute是否在运行中
            execute = Execute.objects.get(pk=case.execute_id)
            if execute.status in ['created', 'ready', 'running']:
                # 跳转到execute的报告页面
                return redirect(to='/execute/%d/' % execute.pk)
            else:
                # 如果不是运行中，那么就直接创建一个新的执行吧
                need_create_execute = True
        else:
            need_create_execute = True

        if need_create_execute:
            # 创建新的execute
            execute_name = case.name + datetime.now().strftime(
                "%Y%m%d%H%M%S")
            execute = Execute.objects.create(case=case, name=execute_name)
            case.execute_id = execute.id
            case.save()
        # 跳转去execute的页面
        return redirect(to='/execute/%d/' % execute.pk)

