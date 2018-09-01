"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

S = r'my/order/daifukuan/'

urlpatterns = [

    # 首页
    url(r'^$', views.index,name="home_index"),
    # 列表
    url(r'^list/(?P<tid>[0-9]+)/$', views.list,name="home_list"),
    # 详情
    url(r'^info/(?P<gid>[0-9]+)/$', views.info,name="home_info"),
    # 注册
    url(r'^register/$', views.register,name="home_register"),
    # 登录
    url(r'^login/$', views.login,name="home_login"),
    # 退出登录
    url(r'^logout/$', views.logout,name="home_logout"),
    # 发送手机验证码
    url(r'^sendSMS/$', views.sendSMS,name="home_sendSMS"),


    # 加入购物车
    url(r'^cart/add/$', views.cartadd,name="home_cartadd"),
    # 购物车列表
    url(r'^cart/list/$', views.cartlist,name="home_cartlist"),
    # 购物车修改
    url(r'^cart/edit/$', views.cartedit,name="home_cartedit"),
    # 删除购物车里的商品
    url(r'^cart/delete/$', views.cartdelete,name="home_cartdelete"),

    # 确定订单
    url(r'^order/confirm/$', views.orderconfirm, name="home_orderconfirm"),
    # 创建订单
    url(r'^order/create/$', views.ordercreate, name="home_ordercreate"),
    # 订单支付
    url(r'^order/buy/$', views.orderbuy, name="home_orderbuy"),


    # 我的订单
    url(r'^my/order/$', views.myorder, name="home_myorder"),
    # 待发货
    url(r'^my/order/daifahuo/$', views.daifahuo, name="home_myorder_daifahuo"),
    # 待付款
    url(r'^%s$' % S, views.daifukuan, name="home_myorder_daifukuan"),
    # 已发货
    url(r'^my/order/yifahuo/$', views.yifahuo, name="home_myorder_yifahuo"),


    # 个人中心
    url(r'^my/centre/$', views.mycentre, name="home_mycentre"),
    # 编辑个人信息
    url(r'^my/useredit/$', views.useredit, name="home_useredit"),
    # 收货地址
    url(r'^address/list/$', views.addresslist, name="home_addresslist"),
    # 添加收货地址
    url(r'^address/insert/$', views.addressinsert, name="home_addressinsert"),
    # 编辑收货地址
    url(r'^address/edit/$', views.addressedit, name="home_addressedit"),
    # 执行编辑收货地址
    url(r'^address/update/$', views.addressupdate, name="home_addressupdate"),
    # 删除收货地址
    url(r'^address/del/$', views.addressdel, name="home_addressdel"),
    # 设置默认地址
    url(r'^address/status/$', views.addressstatus, name="home_addressstatus"),


]

