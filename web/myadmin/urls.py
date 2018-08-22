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
from . views import IndexViews,UserViews


urlpatterns = [
    # 后台主页
    url(r'^$',IndexViews.index,name='myadmin_index'),
    # 后台登录
    url(r'^login/$',IndexViews.myadminlogin,name='myadmin_login'),
    #验证码
    url(r'^verifycode/$',IndexViews.verifycode,name='myadmin_verifycode'),

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
    url(r'^user/status/$',UserViews.status,name='myadmin_user_status'),

]
