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
    url(r'^cartadd/$', views.cartadd,name="home_cartadd"),
    # 购物车列表
    url(r'^cartlist/$', views.cartlist,name="home_cartlist"),
    # 购物车修改
    url(r'^cartedit/$', views.cartedit,name="home_cartedit"),
    # 删除购物车里的商品
    url(r'^cartdelete/$', views.cartdelete,name="home_cartdelete"),


]

