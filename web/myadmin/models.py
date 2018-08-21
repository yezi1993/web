from django.db import models

# Create your models here.
class Users(models.Model):
    # 用户名
    username = models.CharField(max_length=30)
    # 密码
    password = models.CharField(max_length=32)
    # 手机
    # 邮箱
    # 年龄
    # 性别
    # 头像
    # 状态
    # 注册时间
