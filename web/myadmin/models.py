from django.db import models

# Create your models here.
class Users(models.Model):
    # 用户名
    username = models.CharField(max_length=30)
    # 密码
    password = models.CharField(max_length=80)
    # 手机
    phone = models.CharField(max_length=11)
    # 邮箱
    email = models.CharField(max_length=50,null=True)
    # 年龄
    age = models.IntegerField(default=18)
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



class Types(models.Model):
    # 分类名称
    name = models.CharField(max_length=20)
    # 属于哪个分类 0为顶级分类
    pid = models.IntegerField()
    # 记录父级跟自己的id
    path = models.CharField(max_length=30)


class Goods(models.Model):
    # 分类id
    tid = models.ForeignKey(to='Types',to_field='id')
    # 商品名称
    name = models.CharField(max_length=255)
    # 价格
    price = models.FloatField()
    # 商品图片
    pic = models.CharField(max_length=255)
    # 库存
    store = models.IntegerField()
    # 点击量
    clicknum = models.IntegerField(default=0)
    # 订单量
    ordernum = models.IntegerField(default=0)
    # 商品信息
    info = models.TextField()
    # 商品状态 0正常 1下架
    status = models.IntegerField(default=0)
    # 商品添加时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 商品修改时间
    update_time = models.DateTimeField(auto_now=Types)



