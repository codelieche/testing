# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator

from .models import Project
# Create your views here.


class ProjectListView(View):
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
        # 对课程列表进行分页
        # page_num = 1
        # try:
        #     page_num = int(request.GET.get('page', '1'))
        #     print(page_num)
        # except TypeError:
        #     page_num = 1
        page_num = page
        p = Paginator(all_projects, 20)
        projects = p.page(page_num)

        content = {
            'projects': projects,
            'page_num_list': range(1, p.num_pages + 1),
            'last_page': p.num_pages,
        }

        return render(request, 'project/list.html', content)
