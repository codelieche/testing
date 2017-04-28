# -*- coding:utf-8 -*-
"""
tcase app 相关的标签
"""
from django import template

from tproject.models import Project
from ..models import Case, Shiwu

register = template.Library()


@register.inclusion_tag('case/project_shiwu.html')
def get_project_shiwu(pk=0):
    """
    获取项目的所有事务，并返回html
    :param pk:
    :return:
    """
    # 根据项目id获取到相关的所有事务
    if not pk:
        pk = 0
    all_shiwu = Shiwu.objects.filter(project_id=pk)
    return {'all_shiwu': all_shiwu}



