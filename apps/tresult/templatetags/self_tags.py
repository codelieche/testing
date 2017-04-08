# -*- coding:utf-8 -*-
"""
自定义标签
"""
from datetime import datetime

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from tresult.models import Summary

register = template.Library()


@register.filter()
def get_time_sub(time_start, time_end=None):
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
    if not isinstance(value, datetime):
        return ''
    return value.strftime('%Y-%m-%d %H:%M:%S')


@register.inclusion_tag('project/tag_stats.html')
def execute_get_stats(pk):
    summary = Summary.objects.filter(execute_id=pk).last()
    return {'summary': summary}