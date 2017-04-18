# -*- coding:utf-8 -*-
"""
这个文件主要是提供：
1、通过case的id获取到最近的execute id
2、如果最近的execute id是空 就创建一个
"""
from datetime import datetime

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import View
from django.core.exceptions import PermissionDenied

from utils.mixins import CsrfExemptMixin
from ..models import Case, Execute


class CaseExecute(CsrfExemptMixin, View):
    """
    通过Case id获取Execute的View
    # 如果是post，就表示，如果没有就创建一个，然后返回新的execute_id
    """
    def get(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        # 判断是否存在execute id
        if case.execute_id:
            return JsonResponse({'execute_id': case.execute_id})
        else:
            return JsonResponse({'execute_id': None})

    def post(self, request, pk):
        case = get_object_or_404(Case, pk=pk)
        # 判断是否存在execute id
        need_create_execute = False
        if case.execute_id:
            # 根据execute状态来判断这个execute是否可用
            execute = Execute.objects.get(pk=case.execute_id)
            if execute.status in ['failure', 'success', 'stoped']:
                need_create_execute = True
        else:
            need_create_execute = True

        if need_create_execute:
            # 表示还没有execute_id
            # 那就创建一个返回
            execute_name = case.name + datetime.now().strftime("%Y%m%d%H%M%S")
            # 这里由于是post过来的，没做user认证，所以执行者，暂时不设置
            execute = Execute.objects.create(case=case, name=execute_name)
            case.execute_id = execute.id
            # 新建了execute，把Case状态改成Ready
            case.status = 'ready'
            case.save()
        return JsonResponse({'execute_id': case.execute_id})


class ExecuteUpdateStatus(CsrfExemptMixin, View):
    """
    更新Case的状态：
    注意：这个view是在tresult.urls.api_execute中调用的
    # 当测试用例刚保存，状态为created
    # 创建好了case_id.py文件，修改状态为`ready`状态
    # 当开始execute的同时，也修改case的状态为：running
    # execute执行完毕，同时也修改Case的状态为：success / failure / stoped
    # Case还可以删除， 待优化
    """
    def post(self, request, pk):
        execute = get_object_or_404(Execute, pk=pk)
        # 获取执行 对应的Case
        case = execute.case
        status = request.POST.get('status', '')
        status_tuple = ('created', 'ready', 'running',
                        'failure', 'success', 'stoped')
        if status and status in status_tuple:
            # TODO: 这里还要加点安全方面验证，不用登陆，比如每次POST传个密匙即可
            execute.status = status
            if status in ('running', 'stoped', 'failure', 'success'):
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if status == 'running':
                    execute.time_start = now
                else:
                    execute.time_end = now
            execute.save()

        if status in ('running', 'failure', 'success', 'stoped'):
            # 当状态是running、failure、success的时候，也需要更新下case的状态
            case.status = status
            case.save(update_fields=('status',))
        return JsonResponse({"sucess": True})


class CaseDelete(CsrfExemptMixin, View):
    """
    删除CaseView
    """
    # 只有是超级用户才可以删除
    def post(self, request):
        if request.user.is_superuser:

            case_id = request.POST.get('case', '')
            case = get_object_or_404(Case, pk=case_id)
            case.status = 'delete'
            case.save()
            return JsonResponse({'status': "success"})
        else:
            raise PermissionDenied()
