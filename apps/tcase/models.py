# -*- coding:utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from account.models import UserProfile
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
        ('draft', "草稿"),
        ('created', "已创建"),
        ('ready', '准备就绪'),
        ('running', "执行中"),
        ('failure', "有错误"),
        ('success', "成功执行"),
        ('stoped', '已停止'),
        ('delete', "已删除")
    )
    WAY_CHOICES = (
        ('shiwu', "事务"),
        ('code', '代码')
    )
    # 当测试用例刚保存，状态为created
    # 创建好了case_id.py文件，修改状态为`ready`状态, 当新创建了execute也改成ready
    # 当开始execute的同时，也修改case的状态为：running
    # execute执行完毕，同时也修改Case的状态为：success / failure / stoped
    # Case还可以删除， 待优化

    project = models.ForeignKey(to=Project, verbose_name="项目")
    name = models.CharField(max_length=100, verbose_name="测试用例")
    desc = models.CharField(max_length=512, blank=True, verbose_name="描述")
    user = models.ForeignKey(to=UserProfile, blank=True, verbose_name="添加者")

    # 编码方式
    way = models.CharField(max_length=10, choices=WAY_CHOICES, default='shiwu',
                           verbose_name="编码方式")
    # code主要是：get、post访问页面的函数
    code = models.TextField(blank=True, null=True, verbose_name="测试代码")
    # 保存下状态
    status = models.CharField(choices=STATUS_CHOICES, max_length=10,
                              verbose_name="状态", default="created")
    # 保存下最新的execute_id
    execute_id = models.IntegerField(blank=True, null=True,
                                     verbose_name="最近执行")
    # 有些脚本需要cookie信息
    cookies = models.CharField(max_length=512, blank=True, default="")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 由于测试用例后续会修改，需要记录下修改的时间
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间",
                                        blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "测试用例"
        verbose_name_plural = verbose_name

        # 设置Object权限
        # Django会自动添加：add_case, change_case, delete_case权限
        # 通过user.has_perm('tcase.add_case')
        permissions = (
            ('can_view_case', '查看测试用例'),
            ('can_run_case', '执行测试用例'),
        )


@python_2_unicode_compatible
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
    user = models.ForeignKey(to=UserProfile, blank=True, null=True,
                             verbose_name="执行者")
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

        # 添加权限
        permissions = (
            ('can_view_report', '查看测试报告'),
        )


@python_2_unicode_compatible
class Shiwu(models.Model):
    """
    事务Modele
    """
    METHOD_CHOICES = (
        ('get', 'GET'),
        ('post', 'POST'),
        ('put', 'PUT'),
        ('delete', 'DELETE')
    )
    name = models.CharField(max_length=100, verbose_name="事务名")
    project = models.ForeignKey(to=Project, verbose_name="项目")
    # 用例与事务是多对多关系 一个case有多个shiwu，一个shiwu可以用到多个用例中
    # 实务获取case: obj_shiwu.cases.all()
    # 测试用例获取shiwu：obj_case.shiwu_set.all()
    cases = models.ManyToManyField(to=Case, verbose_name="用例")
    is_startup = models.BooleanField(default=False, verbose_name="启动准备")
    method = models.CharField(max_length=10, choices=METHOD_CHOICES,
                              verbose_name="请求方法", default='get')
    url = models.CharField(max_length=100, verbose_name="请求网址")
    cycle = models.BooleanField(default=True, verbose_name="数据可循环")
    body = models.TextField(blank=True, null=True, verbose_name="请求内容")
    user = models.ForeignKey(to=UserProfile, blank=True, null=True,
                             default='', verbose_name="添加者")
    # 请求事务可以克隆，每个人员维护自己的事务
    # 添加测试用例页面可以clone别人的事务
    is_clone = models.BooleanField(default=False, verbose_name="克隆")
    # 克隆母体，因为源头与克隆事务不互相影响，这里不用外键，而是仅保存源事务的ID
    parent = models.IntegerField(blank=True, null=True, default=0,
                                 verbose_name="源头")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "请求事务"
        verbose_name_plural = verbose_name

        # 添加权限
        permissions = (
            ('can_view_shiwu', '查看事务'),
        )
