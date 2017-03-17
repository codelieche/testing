# _*_ coding:utf-8 _*_
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from tcase.models import Case
# Create your models here.


@python_2_unicode_compatible
class Result(models.Model):
    """
    测试结果Model
    """
    case = models.ForeignKey(to=Case, verbose_name="测试用例")
    pass

    def __str__(self):
        return '{0}:测试结果'.format(self.case.name)

    class Meta:
        verbose_name = "测试结果"
        verbose_name_plural = verbose_name
        