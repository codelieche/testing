# -*- coding:utf-8 -*-
"""
tcase app 相关的标签
"""
from django import template

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
    all_shiwu = Shiwu.objects.filter(project_id=pk)
    return {'all_shiwu': all_shiwu, "user": user}
