# _*_ coding:utf-8 _*_
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from utils.storage import ImageStorage
# Create your models here.


@python_2_unicode_compatible
class Case(models.Model):
    """
    性能测试用例Model
    """
    name = models.CharField(max_length=100, verbose_name="测试用例")
    code_num = models.IntegerField(default=0, verbose_name="代码版本")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "测试用例"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class CaseCode(models.Model):
    """
    测试用例代码Model
    """
    # 每个测试用例可以上传多版本的代码，以最新的版本为准
    case = models.ForeignKey(to=Case, verbose_name="测试用例")
    code_file = models.FileField(upload_to='code/content/%y/%m', verbose_name="代码文件",
                                  max_length=100, storage=ImageStorage())
    code_num = models.IntegerField(default=1, verbose_name="代码编号")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")


    def __str__(self):
        return '{0}:code_{1}'.format(self.case.nam, code_num)

    class Meta:
        verbose_name = "测试代码"
        verbose_name_plural = verbose_name
