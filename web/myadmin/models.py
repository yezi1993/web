from django.db import models

# Create your models here.
class Users(models.Model):
    # 用户名
    username = models.CharField(max_length=30)
    # 密码
    password = models.CharField(max_length=32)
    # 手机
    phone = models.CharField(max_length=11)
    # 邮箱
    email = models.CharField(max_length=50)
    # 年龄
    age = models.IntegerField()
    # 性别
    sex = models.CharField(max_length=1,null=True)
    # 头像
    pic = models.CharField(max_length=100,default='/static/pics/user.gif')
    # 状态 0禁用 1启用
    status = models.IntegerField(default=1)
    # 注册时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 修改时间
    update_time = models.DateTimeField(auto_now=True)
