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
    # TODO:详情model需要变更
    STATUS_CHOICES = (
        ('running', "运行中"),
        ("stoped", "停止"),
    )
    execute = models.ForeignKey(to=Execute, verbose_name="用例执行")
    # content = models.TextField(verbose_name="运行结果")
    user_count = models.IntegerField(default=0, verbose_name="并发用户数")
    time_avg = models.FloatField(default=0, verbose_name="响应时间")
    total_rps = models.FloatField(default=0.0, verbose_name="每秒处理数")
    fail_ratio = models.FloatField(default=0.00, verbose_name="失败率")
    num_requests = models.IntegerField(default=0, verbose_name="总共请求数")
    num_failures = models.IntegerField(default=0, verbose_name="失败请求数")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='running', verbose_name="状态")
    add_time = models.DateTimeField(verbose_name="时间")

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
    STATUS_CHOICES = (
        ('running', "运行中"),
        ("stoped", "停止"),
    )
    execute = models.ForeignKey(to=Execute, blank=True, verbose_name="用例执行")
    user_count = models.IntegerField(default=0, verbose_name="并发用户数")
    total_rps = models.FloatField(default=0.0, verbose_name="每秒处理数量")
    fail_ratio = models.FloatField(default=0.00, verbose_name="失败率")
    time_min = models.FloatField(default=0, verbose_name="最快响应时间")
    time_avg = models.FloatField(default=0, verbose_name="平均响应时间")
    time_midian = models.FloatField(default=0, verbose_name="响应(中位数)")
    time_max = models.FloatField(default=0, verbose_name="最慢响应时间")
    num_requests = models.IntegerField(default=0, verbose_name="总共请求数")
    num_failures = models.IntegerField(default=0, verbose_name="失败请求数")
    status = models.CharField(choices=STATUS_CHOICES, max_length=10,
                              default='running', verbose_name="状态")

    add_time = models.DateTimeField(verbose_name="添加时间")

    def save(self, *args, **kwargs):
        """
        对象保存前对float字段取2位数
        :return:
        """
        # print(self.time_avg, 'time_avg', type(self.time_avg))
        self.time_avg = round(self.time_avg, 2)
        super(Summary, self).save(*args, **kwargs)

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
    add_time = models.DateTimeField(verbose_name="添加时间")

    def __str__(self):
        return '{0}_{1}'.format(self.execute.name, self.csv_type)

    class Meta:
        verbose_name = "执行结果统计"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class Log(models.Model):
    """
    执行日志Model
    记录 测试过程中的日志：添加并发用户数，错误日志啊
    在数据收集脚本中设置，出错N次就停止测试
    在性能测试过程中，我们需要对错误的日志进行记录
    """
    TYPE_CHOICES = (
        ('start', "开始"),
        ('info', "信息"),
        ('error', "错误"),
        ('stop', "停止")
    )
    # execute ： start、info、error、stop都需要记录
    execute = models.ForeignKey(to=Execute, verbose_name="用例执行")
    content = models.TextField(verbose_name="日志内容")
    log_type = models.CharField(choices=TYPE_CHOICES, max_length=10,
                                verbose_name="日志类型")
    add_time = models.DateTimeField(verbose_name="添加时间")

    def __str__(self):
        return "{}:log:{}".format(self.execute.name, self.add_time)

    class Meta:
        verbose_name = "执行日志"
        verbose_name_plural = verbose_name
