# -*- coding:utf-8 -*-
import os
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse

from tproject.models import Project
from utils.mixins import LoginRequiredMixin
from utils.make_case_file import make_case_file
from ..models import Case, Execute
from ..forms import CaseForm

# Create your views here.


class CaseListView(View):
    """
    网站首页View
    """
    def get(self, request, page=None):
        all_case = Case.objects.all()
        # 关键词过滤
        keyword = request.GET.get('keyword', '')
        if keyword :
            projects = Project.objects.filter(Q(name__icontains=keyword) |
                                              Q(address__icontains=keyword) |
                                              Q(name_en__icontains=keyword))
            all_case = all_case.filter(Q(project__in=projects) |
                                       Q(name__icontains=keyword))

        # 分页处理
        if page:
            page_num = page
        else:
            page_num = 1
        p = Paginator(all_case, 10)
        cases = p.page(page_num)

        return render(request, 'case/list.html', {
            'all_case': cases,
            'page_num_list': range(1, p.num_pages + 1),
            'last_page': p.num_pages,
            'keyword': keyword,
        })


class CaseExecuteView(LoginRequiredMixin, View):
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
        # 这里还需要对user进行权限判断，是否有执行的权限：
        user = request.user
        # TODO：权限判断

        # 第一步：先判断case_id.py的文件是否存在
        base_dir_parent = os.path.dirname(settings.BASE_DIR)
        scripts_dir = os.path.join(base_dir_parent, 'scripts')
        case_file_name = 'case_%s.py' % pk
        case_file_path = os.path.join(scripts_dir, case_file_name)
        # 判断文件是否存在
        if os.path.exists(case_file_path):
            # 如果存在，删除文件
            os.remove(case_file_path)
        # 每次都写入新的文件，以为脚本中可能会有cookies
        host_target = request.META['HTTP_HOST']
        case_code = case.code
        # 如果代码中有COOKIES_FOR_REPLACE 且 cookies不为空，就替换
        # 注意："COOKIES_FOR_REPLACE" 以后在脚本中的set_up中的cookie就写成这个
        if case_code.find("COOKIES_FOR_REPLACE") > 0 and case.cookies:
            case_code = case_code.replace("COOKIES_FOR_REPLACE", case.cookies)
        result = make_case_file(
            code_content=case_code,
            file_name=case_file_name,
            case_id=pk,
            host_target=host_target
        )
        # 如果result是False就需要抛出500错误:报个403吧
        if not result:
            raise PermissionDenied

        # 第二步：判断execute_id是否存在, 判断是否要创建新的execute
        need_create_execute = False
        execute = None
        # 判断是否存在execute id
        if case.execute_id:
            # 有execute_id字段 还需要判断这个execute是否在运行中
            execute = Execute.objects.filter(pk=case.execute_id).last()
            if execute and execute.status in ['created', 'ready', 'running']:
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
            # 同时要记录是谁执行的
            execute = Execute.objects.create(case=case, name=execute_name,
                                             user=user)
            case.execute_id = execute.id
            case.save()
        # 跳转去execute的页面
        return redirect(to='/execute/%d/' % execute.pk)


class CaseAddView(LoginRequiredMixin, View):
    """
    添加测试用例View
    需要登陆
    """
    def get(self, request):
        # 先获取到所有项目
        all_projects = Project.objects.all()
        # 获取get project 的id, 前台根据这个选中默认的project
        project = request.GET.get('project', '')
        # 也可以根据id或者英文名字匹配出第一个项目
        target_project = None
        if project:
            if project.isdigit():
                target_project = Project.objects.filter(pk=project).first()
            else:
                target_project = Project.objects.filter(
                    name_en__icontains=project).first()
                # 如果传入了project字符，也对项目进行过滤一下
                all_projects = all_projects.filter(name_en__icontains=project)

        target_project_id = 0
        if target_project:
            target_project_id = target_project.pk

        return render(request, 'case/add.html', {
            'all_projects': all_projects,
            'target_project': target_project_id
        })

    def post(self, request):
        # post添加case
        # 因为case需要user字段，但是user_id不从前端传入，直接去request.user.pk
        # 这样在实例化CaseForm的时候，传入个instance对象
        case = CaseForm(request.POST, instance=Case(user_id=request.user.pk))
        # print(case)
        if case.is_valid():
            # 传入的数据ok
            # print(case.data, case.data['project'])
            case.save()
        else:
            # 传入的数据不正确
            print(case.errors)
        return redirect(reverse('project:detail', args=[case.data['project']]))


class CaseEditView(View):
    """
    测试用例编辑View
    """
    def get(self, request, pk):
        # 先获取到case实例对象
        case = get_object_or_404(Case, pk=pk)
        return render(request, 'case/edit.html', {
            'case': case,
            'status_choices': Case.STATUS_CHOICES,
        })

    def post(self, request, pk):
        # 先获取到case实例对象
        case = get_object_or_404(Case, pk=pk)
        # 实例化CaseForm
        case_form = CaseForm(request.POST, instance=case)

        if case_form.is_valid():
            # 保存新的case
            case_new = case_form.save()
            return redirect(to=reverse('project:detail',
                                       args=(case_new.project_id,)))
        else:
            # 验证失败
            return redirect(to=reverse('case:edit', args=(pk,)))
