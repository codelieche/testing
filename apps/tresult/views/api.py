# -*- coding:utf-8 -*-
"""
这个是收集测试结果数据的api
"""

from django.views.generic import View
from django.http import JsonResponse

from tresult.models import StatsCSV, Summary
from tresult.forms.apis import StatsCSVForm, SummaryForm
from utils.mixins import CsrfExemptMixin


class AddStatsView(CsrfExemptMixin, View):
    """
    统计csv数据View
    """

    def get(self, request):
        return JsonResponse({"stats": []})

    def post(self, request):
        """
        post过来的数据，主要就是一个type和内容,执行测试的id
        """
        # 先实例化 统计form
        stats_csv_form = StatsCSVForm(request.POST)
        # 对表单进行验证
        if stats_csv_form.is_valid():
            StatsCSV.objects.create(
                    execute_id=stats_csv_form.cleaned_data['execute'],
                    csv_type=stats_csv_form.cleaned_data['csv_type'],
                    content=stats_csv_form.cleaned_data['content']
                )
            return JsonResponse({'status': "success", "msg": "添加成功"})
        else:
            return JsonResponse({'status': "error", "msg": "添加失败"})


class AddSummaryView(CsrfExemptMixin, View):
    """添加Summary View"""
    def get(self, request):
        return JsonResponse({"status": "success"})

    def post(self, request):
        # 先实例化summary表单
        summary_form = SummaryForm(request.POST)
        # print(summary_form)
        if summary_form.is_valid():
            summary_form.save()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse(
                {
                  "status": "error",
                  'msg': summary_form.errors
                }
            )