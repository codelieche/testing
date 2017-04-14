# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.core.paginator import Paginator
from django.db.models import Q

from utils.mixins import CsrfExemptMixin
from tcase.models import Execute
from tresult.models import Summary

from .models import Project
# Create your views here.


class ProjectListView(CsrfExemptMixin, View):
    """
    项目列表View
    """
    def get(self, request, page=1):
        """
        :param request:
        :param page: 页码
        :return:
        """
        all_projects = Project.objects.all()

        # 关键字过滤
        keyword = request.GET.get('keyword', '')
        if keyword:
            all_projects = all_projects.filter(
                Q(name__icontains=keyword) |
                Q(address__icontains=keyword) |
                Q(name_en__icontains=keyword)
            )

        # 对课程列表进行分页
        page_num = page
        p = Paginator(all_projects, 10)
        projects = p.page(page_num)

        content = {
            'projects': projects,
            'page_num_list': range(1, p.num_pages + 1),
            'last_page': p.num_pages,
            'keyword': keyword,
        }

        return render(request, 'project/list.html', content)


class ProjectDetailView(View):
    """
    项目详情页View
    """
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)

        # 测试用例列表
        all_case = project.case_set.all()

        # 测试结果列表
        # 获取all_case的id
        all_execute = Execute.objects.filter(case__in=all_case,
                                             status__in=['stoped', 'sucess'])
        all_execute_id = []
        all_report = Summary.objects.filter(
            execute__in=all_execute).order_by('-add_time')
        return render(request, 'project/detail.html', {
            "project": project,
            'all_case': all_case,
            'all_report': all_report,
        })
