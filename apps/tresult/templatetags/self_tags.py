# -*- coding:utf-8 -*-
"""
自定义标签
"""
from datetime import datetime

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from tcase.models import Case, Execute
from tresult.models import Summary

register = template.Library()


@register.filter()
def get_time_sub(time_start, time_end=None):
    """
    获取两个时间的时间差:
    :param time_start: 开始时间
    :param time_end: 结束时间
    :return: 16分3秒
    """
    if not time_end:
        time_end = datetime.now()
    if not isinstance(time_start, datetime) or \
            not isinstance(time_end, datetime):
        return ''
    time_sub = time_end - time_start
    seconds = time_sub.seconds
    miao = seconds % 60
    fen = int(seconds / 60)
    if fen > 60:
        fen %= 60
    shi = int(seconds / (60 * 60))
    if shi > 0:
        return '{}时{}分{}秒'.format(shi, fen, miao)
    else:
        return '{}分{}秒'.format(fen, miao)


@register.filter()
def strf_time(value):
    """
    格式化时间：2017-04-07 10:30:13
    :param value:
    :return:
    """
    if not isinstance(value, datetime):
        return ''
    return value.strftime('%Y-%m-%d %H:%M:%S')


@register.inclusion_tag('project/tag_stats.html')
def execute_get_stats(pk):
    """
    execute的统计信息，Html
    :param pk: execute id
    :return: 是html内容，在Project detail中用到
    """
    summary = Summary.objects.filter(execute_id=pk).last()
    return {'summary': summary}


@register.filter()
def get_project_report_num(project_id):
    """
    获取项目的报告数:
    在Project list中用到
    :param project_id:
    :return:
    """
    # 先获取到测试用例
    all_case = Case.objects.filter(project_id=project_id)
    # 获取出execute
    all_execute_count = Execute.objects.filter(
        case__in=all_case, status='stoped').count()
    return all_execute_count


@register.assignment_tag(name="get_latest_report")
def get_latest_report(count=5):
    """
    返回最近的报告
    :param count: 返回的数量
    :return: 返回的是一个数组，可以在模版中用for标签使用
    """
    latest_report = Execute.objects.filter(
        status='stoped').order_by('-time_end')[:count]
    return latest_report


@register.assignment_tag(name="get_latest_cases")
def get_latest_cases(count=5):
    """
    获取最新的测试用例
    :param count: 获取数量默认5
    :return:
    """
    latest_cases = Case.objects.order_by('-add_time')[:count]
    return latest_cases
