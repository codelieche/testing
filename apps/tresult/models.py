# _*_ coding:utf-8 _*_
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from tcase.models import Execute
# Create your models here.


"""
每次测试用例代码的执行，都需要记录结果，和摘要信息
"""

@python_2_unicode_compatible
class Result(models.Model):
    """
    测试结果Model
    """
    execute = models.ForeignKey(to=Execute, verbose_name="用例执行")
    pass

    def __str__(self):
        return '{0}:执行结果'.format(self.execute.name)

    class Meta:
        verbose_name = "执行结果"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class Summary(models.Model):
    """
    测试摘要Model
    并发数、TPS(每秒吞吐量)、失败率、响应时间
    """
    execute = modules.ForeignKey(to=Execute, verbose_name="用例执行")
    user_num = models.IntegerField(default=0, verbose_name="并发用户数")
    tps = models.IntegerField(default=0, verbose_name="每秒处理笔数")
    per_fail = models.FloatField(default=0.0, verbose_name="失败率")
    time = models.FloatField(default=0, verbose_name="响应时间")
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
            'request', "请求统计",
            'request', "响应统计",
            'exception', "异常统计",
        )
    execute = modules.ForeignKey(to=execute, verbose_name="用例执行")
    csv_type = models.CharField(choices=CSV_TYPE_CHOICES, max_length=10,
                                verbose_name="结果类型")
    # 统计内容是csv格式的，后面再做处理
    content = models.TextField(verbose_name="统计内容")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def __str__(self):
        return self.csv_type

    class Meta:
        verbose_name = "执行结果统计"
        verbose_name_plural = verbose_name





