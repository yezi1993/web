from django.db import models

# 前台用户表
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
    sex = models.CharField(max_length=1,default='1')
    # 头像
    pic = models.CharField(max_length=100,default='/static/pics/user.gif')
    # 状态 0禁用 1启用
    status = models.IntegerField(default=1)
    # 注册时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 修改时间
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("show_users", "会员查看权限"),
            ("insert_users", "会员添加权限"),
            ("remove_users", "会员删除权限"),
            ("update_users", "会员修改权限"),
        )

# 商品分类表
class Types(models.Model):
    # 分类名称
    name = models.CharField(max_length=20)
    # 属于哪个分类 0为顶级分类
    pid = models.IntegerField()
    # 记录父级跟自己的id
    path = models.CharField(max_length=30)

    class Meta:
        permissions = (
            ("show_types", "商品分类查看权限"),
            ("insert_types", "商品分类添加权限"),
            ("remove_types", "商品分类删除权限"),
            ("update_types", "商品分类修改权限"),
        )

# 商品表
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

    class Meta:
        permissions = (
            ("show_goods", "商品查看权限"),
            ("insert_goods", "商品添加权限"),
            ("remove_goods", "商品删除权限"),
            ("update_goods", "商品修改权限"),
        )

# 收货地址表
class Address(models.Model):
    # 用户 收货人 收货地址 收货电话  备注 是否默认地址
    uid = models.ForeignKey(to="Users", to_field="id")
    aname = models.CharField(max_length=10)
    ads = models.CharField(max_length=100)
    aphone = models.CharField(max_length=11)
    atags = models.CharField(max_length=10,null=True)
    isstatus = models.BooleanField(default=False)

# 订单表
class Order(models.Model):
    uid = models.ForeignKey(to="Users", to_field="id")
    aid = models.ForeignKey(to="Address", to_field="id")
    totalprice = models.FloatField()
    # 0 未支付, 1已支付,2,已发货,3已收货,4,已取消
    status  = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ("show_order", "订单查看权限"),
            ("update_order", "订单修改权限"),
        )

# 订单详情表
class OrderInfo(models.Model):
    orderid =  models.ForeignKey(to="Order", to_field="id")
    gid = models.ForeignKey(to="Goods", to_field="id")
    num  = models.IntegerField()
    price = models.FloatField()


# 城市表
class Citys(models.Model):
    name = models.CharField(max_length=20)
    level = models.IntegerField()
    upid = models.IntegerField()

