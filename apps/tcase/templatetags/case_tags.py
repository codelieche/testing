# -*- coding:utf-8 -*-
"""
tcase app 相关的标签
"""
from django import template
from django.db.models import F

from tproject.models import Project
from ..models import Case, Shiwu

register = template.Library()


@register.inclusion_tag('case/project_shiwu.html')
def get_project_shiwu(pk=0, user=None):
    """
    获取项目的所有事务，并返回html
    :param pk: 项目的主键，id
    :param 请求用户，标签模版中不能使用request.user获取用户，所以传递user值
    :return:
    """
    # 根据项目id获取到相关的所有事务
    if not pk:
        pk = 0
    # 获取所有的项目的事务，是当前用户的事务排在前面
    if user:
        all_shiwu = Shiwu.objects.filter(project_id=pk).annotate(
            owner=(F('user_id') - user.pk)).order_by('owner')
    else:
        all_shiwu = Shiwu.objects.filter(project_id=pk)
    # 需要排除，已经克隆了的
    cloned_shiwu = Shiwu.objects.filter(is_clone=True, project_id=pk)
    cloned_shiwu_ids = [i.parent for i in cloned_shiwu]
    # 排除all_shiwu中的克隆的母体
    all_shiwu = all_shiwu.exclude(id__in=cloned_shiwu_ids)
    return {'all_shiwu': all_shiwu, "user": user}
