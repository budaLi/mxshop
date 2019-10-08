from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#注意此处需要在设置中更改系统用户  AUTH_USER_MODEL = 'user.UserProfile'
class UserProfile(AbstractUser):
    """
    用户信息表
    """
    # blank表示字段存储的是一个空字符串 默认为flase 如果设置为true的话表示该字段必须填写
    # 而null表示数据库中该字段可以为null 日期类型和数字类型不能接受空字符串 如果要设置 则必须同时设置null=True blank=True
    # 也就是说null=True是针对数据库的
    # blank=True 是针对表单的 也就是填写表单时该字段可以不填

    #当注册时只需要邮箱或者手机号进行注册 用户名无法填写 在这里设置可以为空
    name = models.CharField(max_length=30,null=True,blank=True,verbose_name='姓名')
    birthday=models.DateField(null=True,blank=True,verbose_name='出生年月')
    gender=models.CharField(max_length=6,choices=(('male',u'男'),('female',u'女')),default='female',verbose_name='性别')

    #邮箱设置为空和name设置为空理由一致
    mobile=models.CharField(max_length=11,verbose_name='手机号')
    email = models.CharField(max_length=100,null=True,blank=True,verbose_name='邮箱')

    #注册时间 一般所有的表都会有添加时间
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    #后台管理时显示数据库名字
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    #python3中已经不存在unicode编码的概念
    def __str__(self):
        return self.name


class VerifyCode(models.Model):
    """
    短信验证码
    在这里可以采用将验证码设置在内存中 用redis实现 也可以将验证码存储在数据库中
    """
    code=models.CharField(max_length=10,verbose_name='验证码')
    mobile=models.CharField(max_length=11,verbose_name='电话号码')
    add_time=models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='短信验证码'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.code