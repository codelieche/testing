# -*- coding:utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from tproject.models import Project
from utils.storage import ImageStorage
# Create your models here.


@python_2_unicode_compatible
class Case(models.Model):
    """
    性能测试用例Model
    """
    # 状态选项，如果是running，就不创建新的执行
    STATUS_CHOICES = (
        ('created', "已创建"),
        ('ready', '准备就绪'),
        ('running', "执行中"),
        ('failure', "有错误"),
        ('success', "成功执行"),
        ('stoped', '已停止'),
        ('delete', "已删除")
    )
    # 当测试用例刚保存，状态为created
    # 创建好了case_id.py文件，修改状态为`ready`状态, 当新创建了execute也改成ready
    # 当开始execute的同时，也修改case的状态为：running
    # execute执行完毕，同时也修改Case的状态为：success / failure / stoped
    # Case还可以删除， 待优化

    project = models.ForeignKey(to=Project, verbose_name="项目")
    name = models.CharField(max_length=100, verbose_name="测试用例")
    desc = models.CharField(max_length=512, blank=True, verbose_name="描述")

    # code主要是：get、post访问页面的函数
    code = models.TextField(blank=True, null=True, verbose_name="测试代码")
    # 保存下状态
    status = models.CharField(choices=STATUS_CHOICES, max_length=10,
                              verbose_name="状态", default="created")
    # 保存下最新的execute_id
    execute_id = models.IntegerField(blank=True, null=True,
                                     verbose_name="最近执行")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "测试用例"
        verbose_name_plural = verbose_name


class Execute(models.Model):
    """
    测试用例执行Model
    """
    STATUS_CHOICES = (
        ('created', "已创建"),
        ('ready', "已准备"),
        ('running', "运行中"),
        ('failure', "失败"),
        ('success', "成功"),
        ('stoped', "已停止")
    )
    # Case执行，先创建Execute，这个时候状态是created
    # 进入执行，状态变为ready
    # 开始执行，修改状态为：running
    # locust触发了stop事件的时候，修改状态为：success / failure / stoped

    # name规范：测试用例版本N第n次执行
    name = models.CharField(max_length=100, blank=True, verbose_name="执行名字")
    case = models.ForeignKey(to=Case, verbose_name="测试用例")
    # 状态
    status = models.CharField(max_length=10, verbose_name="状态",
                              default="created")
    port = models.IntegerField(default=8089, verbose_name="locust端口号")
    time_start = models.DateTimeField(blank=True, null=True,
                                      verbose_name="开始时间")
    time_end = models.DateTimeField(blank=True, null=True,
                                    verbose_name="结束时间")

    def __str__(self):
        # return '{0}:测试结果'.format(self.code.case.name)
        return self.name

    class Meta:
        verbose_name = "执行测试"
        verbose_name_plural = "执行测试列表"


@python_2_unicode_compatible
class CaseCode(models.Model):
    """
    测试用例代码Model
    """
    # 每个测试用例可以上传多版本的代码，以最新的版本为准
    case = models.ForeignKey(to=Case, verbose_name="测试用例")
    code_file = models.FileField(upload_to='code/content/%y/%m',
                                 verbose_name="代码文件", max_length=100,
                                 storage=ImageStorage())
    code_num = models.IntegerField(default=1, verbose_name="代码编号")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return '{0}:code_{1}'.format(self.case.name, self.code_num)

    class Meta:
        verbose_name = "测试代码"
        verbose_name_plural = verbose_name


