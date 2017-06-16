# -*- coding:utf-8 -*-
"""
测试执行相关的api
"""
import datetime

from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from utils.mixins import CsrfExemptMixin
from tcase.models import Execute


class ExecuteDeleteApiView(CsrfExemptMixin, View):
    """删除execute View"""

    def delete(self, request, pk):
        # 先获取到对应的execute
        execute = get_object_or_404(Execute, pk=pk)
        # 删除一定要最权限进行判断，而且只有自己可以删除
        if request.user == execute.user:
            # 会把对应的log、detail、statcsv、summary信息全部删除
            # 而且只能24h内可以删除
            time_end = execute.time_end
            try:
                time_deleta = datetime.datetime.now() - time_end
                if time_deleta.days < 1:
                    # 对待delete操作要特别谨慎
                    execute.delete()
                    msg = "删除[{}]成功".format(execute)
                else:
                    print("超过24h了，只有管理员可已删除")
                    msg = "超过24h了，只有管理员可已删除"
            except Exception as e:
                print(e)
                msg = "删除异常：{}".format(e)
        else:
            raise PermissionDenied
        content = {
            "status": "success",
            "message": msg
        }
        return JsonResponse(content)

