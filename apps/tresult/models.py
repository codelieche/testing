# -*- coding:utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from tcase.models import Execute
# Create your models here.

"""
每次测试用例代码的执行，都需要记录结果，和摘要信息
"""


@python_2_unicode_compatible
class Detail(models.Model):
    """
    测试结果详情Model
    """
    STATE_CHOICES = (
        ('running', "运行中"),
        ("stoped", "停止中"),
    )
    execute = models.ForeignKey(to=Execute, verbose_name="用例执行")
    content = models.TextField(verbose_name="运行结果")
    add_time = models.DateTimeField(verbose_name="时间")
    state = models.CharField(max_length=10, choices=STATE_CHOICES,
                             default='running', verbose_name="状态")

    def __str__(self):
        return '{0}:执行结果'.format(self.execute.name)

    class Meta:
        verbose_name = "执行结果"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class Summary(models.Model):
    """
    测试摘要Model
    并发数、RPS(每秒吞吐量)、失败率、响应时间
    """
    STATE_CHOICES = (
        ('running', "运行中"),
        ("stoped", "停止中"),
    )
    execute = models.ForeignKey(to=Execute, blank=True, verbose_name="用例执行")
    user_count = models.IntegerField(default=0, verbose_name="并发用户数")
    total_rps = models.FloatField(default=0.0, verbose_name="每秒处理数量")
    fail_ratio = models.FloatField(default=0.0, verbose_name="失败率")
    time_min = models.FloatField(default=0, verbose_name="最快响应时间")
    time_avg = models.FloatField(default=0, verbose_name="平均响应时间")
    time_midian = models.FloatField(default=0, verbose_name="响应(中位数)")
    time_max = models.FloatField(default=0, verbose_name="最慢响应时间")
    num_requests = models.IntegerField(default=0, verbose_name="总共请求数")
    num_failures = models.IntegerField(default=0, verbose_name="失败请求数")
    state = models.CharField(choices=STATE_CHOICES, max_length=10,
                             default='running', verbose_name="状态")

    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def __str__(self):
        return self.execute.name + ":summary"

    class Meta:
        verbose_name = "执行摘要"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class StatsCSV(models.Model):
    """
    CSV结果摘要Model
    统计摘要、异常数据、响应数据
    当测试执行结束的时候触发添加事件
    """
    CSV_TYPE_CHOICES = (
            ('request', "请求统计"),
            ('response', "响应统计"),
            ('exception', "异常统计"),
        )
    execute = models.ForeignKey(to=Execute, verbose_name="用例执行")
    csv_type = models.CharField(choices=CSV_TYPE_CHOICES, max_length=10,
                                verbose_name="结果类型")
    # 统计内容是csv格式的，后面再做处理
    content = models.TextField(verbose_name="统计内容")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def __str__(self):
        return '{0}_{1}'.format(self.execute.name, self.csv_type)

    class Meta:
        verbose_name = "执行结果统计"
        verbose_name_plural = verbose_name

