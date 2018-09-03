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
from .views import IndexViews, UserViews, TypesViews, GoodsViews, AuthViews, OrderViews, SlideshowViews

urlpatterns = [

    # 后台主页
    url(r'^$', IndexViews.index, name='myadmin_index'),
    # 后台登录
    url(r'^login/$', IndexViews.myadminlogin, name='myadmin_login'),
    # 后台退出
    url(r'^logout/$', IndexViews.myadminlogout, name='myadmin_logout'),
    # 验证码
    url(r'^verifycode/$', IndexViews.verifycode, name='myadmin_verifycode'),

    # 后台管理员页
    url(r'^auth/user/index/$', AuthViews.userindex, name='myadmin_auth_userindex'),
    # 管理员添加
    url(r'^auth/user/add/$', AuthViews.useradd, name='myadmin_auth_useradd'),
    # 管理员修改页
    url(r'^auth/user/edit/$', AuthViews.useredit, name='myadmin_auth_useredit'),
    # 管理员修改执行
    url(r'^auth/user/update/$', AuthViews.userupdate, name='myadmin_auth_userupdate'),
    # 管理员删除
    url(r'^auth/user/del/$', AuthViews.userdel, name='myadmin_auth_userdel'),

    # 管理组列表页
    url(r'^auth/group/index/$', AuthViews.groupindex, name="myadmin_auth_groupindex"),
    # 管理组添加
    url(r'^auth/group/add/$', AuthViews.groupadd, name="myadmin_auth_groupadd"),
    # 管理组修改
    url(r'^auth/group/edit/$', AuthViews.groupedit, name="myadmin_auth_groupedit"),
    # 管理组修改执行
    url(r'^auth/group/update/$', AuthViews.groupupdate, name="myadmin_auth_groupupdate"),
    # 管理组删除
    url(r'^auth/group/del/$', AuthViews.groupdel, name="myadmin_auth_groupdel"),

    # 用户列表页
    url(r'^user/index/$', UserViews.index, name='myadmin_user_index'),
    # 用户添加
    url(r'^user/add/$', UserViews.add, name='myadmin_user_add'),
    # 用户编辑
    url(r'^user/edit/(?P<uid>[0-9]+)/$', UserViews.edit, name='myadmin_user_edit'),
    # 用户编辑处理
    url(r'^user/update/$', UserViews.update, name='myadmin_user_update'),
    # 用户删除
    url(r'^user/delete/$', UserViews.delete, name='myadmin_user_del'),
    # 修改用户状态
    url(r'^user/status/$', UserViews.status, name='myadmin_user_status'),

    # 分类列表页
    url(r'^types/index/$', TypesViews.index, name='myadmin_types_index'),
    # 分类添加
    url(r'^types/add/$', TypesViews.add, name='myadmin_types_add'),
    # 分类删除
    url(r'^types/delete/$', TypesViews.delete, name='myadmin_types_del'),
    # 修改分类名称
    url(r'^types/edit/$', TypesViews.edit, name='myadmin_types_edit'),

    # 商品管理
    url(r'^goods/add/', GoodsViews.add, name='myadmin_goods_add'),
    # 商品主页
    url(r'^goods/index/', GoodsViews.index, name='myadmin_goods_index'),
    # 商品编辑
    url(r'^goods/edit/(?P<uid>[0-9]+)/$', GoodsViews.edit, name='myadmin_goods_edit'),
    # 商品执行编辑
    url(r'^goods/update/$', GoodsViews.update, name='myadmin_goods_update'),
    # 商品删除
    url(r'^goods/delete/$', GoodsViews.delete, name='myadmin_goods_delete'),
    # 商品是否热销
    url(r'^goods/rexiao/$', GoodsViews.rexiao, name='myadmin_goods_rexiao'),

    # 订单列表
    url(r'^orders/index/', OrderViews.index, name='myadmin_orders_index'),
    # 订单详情
    url(r'^orders/ordersinfo/', OrderViews.ordersinfo, name='myadmin_orders_ordersinfo'),
    # 修改订单状态
    url(r'^orders/orderstatus/', OrderViews.orderstatus, name='myadmin_orders_orderstatus'),

    # 轮播图管理
    url(r'^slidesshow/add/', SlideshowViews.add, name='myadmin_slidesshow_add'),
    # 轮播图主页
    url(r'^slidesshow/index/', SlideshowViews.index, name='myadmin_slidesshow_index'),
    # 轮播图编辑
    url(r'^slidesshow/edit/(?P<sid>[0-9]+)/$', SlideshowViews.edit, name='myadmin_slidesshow_edit'),
    # 轮播图执行编辑
    url(r'^slidesshow/update/$', SlideshowViews.update, name='myadmin_slidesshow_update'),
    # 轮播图删除
    url(r'^slidesshow/delete/(?P<id>[0-9]+)/$', SlideshowViews.delete, name='myadmin_slidesshow_delete'),
    # 轮播图修改状态
    url(r'^slidesshow/status/$', SlideshowViews.status, name='myadmin_slidesshow_status'),
]
