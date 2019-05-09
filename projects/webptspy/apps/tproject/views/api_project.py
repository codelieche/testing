# -*- coding:utf-8 -*-
"""
Project api相关的视图
"""
from django.http import JsonResponse
from django.views.generic import View

from tproject.models import Project, ServerInfo
from utils.mixins import CsrfExemptMixin

from ..forms import ServerInfoModelForm


class ProjectListApiView(View):
    """
    项目列表信息api View
    """
    def get(self, request):
        all_project = Project.objects.all()
        results = []
        for project in all_project:
            results.append({
                "id": project.pk,
                "name_en": project.name_en
            })

        content = {"results": results}
        return JsonResponse(content)


class UpdateProjectServerInfoApiView(CsrfExemptMixin, View):
    """
    更新或者插入项目服务信息api View
    """
    def post(self, request):
        # 字段：test_db, product_db, test_deployment, product_deployment
        #      test_server, product_server
        # 获取数据
        project_id = request.POST.get('project', '')
        if not project_id:
            return JsonResponse({'result': False}, status=400)

        serverinfo = ServerInfo.objects.filter(project_id=project_id).first()
        # 如果serverinfo存在
        if serverinfo:
            form = ServerInfoModelForm(data=request.POST, instance=serverinfo)
            if form.is_valid():
                form.save()
                result = True
            else:
                result = False
        else:
            # 不存在就重新创建咯
            form = ServerInfoModelForm(data=request.POST)
            if form.is_valid():
                form.save()
                result = True
            else:
                result = False

        # 返回结果：
        if result:
            content = {"result": "success"}
            return JsonResponse(content)
        else:
            content = {"result": False}
            return JsonResponse(content, status=400)
