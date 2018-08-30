from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import permission_required

# 后台管理员添加
@permission_required('auth.add_user',raise_exception=True)
def useradd(request):
    if request.method == 'POST':
        # 获取所有表单提交的数据
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        # 判断是不是超级管理员
        if data['is_superuser'] == '1':
            data['is_superuser'] = True
            ob = User.objects.create_superuser(**data)
        else:
            data['is_superuser'] = False
            ob = User.objects.create_user(**data)

        # 给用户分配管理组
        gs = request.POST.getlist('gs', None)
        if gs:
            gs = Group.objects.filter(id__in=gs)
            ob.groups.set(gs)

        return HttpResponse("<script>location.href='/myadmin/auth/user/index'</script>")
    else:

        return render(request, 'myadmin/auth/add.html')


# 后台管理员列表
@permission_required('auth.add_user',raise_exception=True)
def userindex(request):
    # 获取所有用户数据
    data = User.objects.all()

    return render(request,'myadmin/auth/index.html',{'data':data})

# 后台管理员修改页
@permission_required('auth.add_user',raise_exception=True)
def useredit(request):
    # 获取管理员id
    uid = request.GET.get('uid')
    # 获取对象
    ob = User.objects.get(id=uid)

    # 获取当前用户选择的组之外的组
    gs = Group.objects.exclude(id__in=ob.groups.all())

    # 分配数据
    context = {'data':ob,'glist':gs}
    # 加载模板
    return render(request,'myadmin/auth/edit.html',context)

# 执行后台管理员修改
@permission_required('auth.add_user',raise_exception=True)
def userupdate(request):
    # 获取修改的管理员id
    ob = User.objects.get(id=request.POST['uid'])
    # 获取修改信息
    ob.username = request.POST['username']
    if request.POST.get('password', None):
        ob.password = make_password(request.POST['password'])
    ob.email = request.POST['email']

    if request.POST['is_superuser'] == '1':
        ob.is_superuser = True
    else:
        ob.is_superuser = False
    # /管理员更新
    ob.save()

    # 先清空组
    ob.groups.clear()

    # 管理员所在组
    gs = request.POST.getlist('gs', None)
    if gs:
        # 把新加的组入库
        ob.groups.set(Group.objects.filter(id__in=gs))

    return HttpResponse('<script>location.href="/myadmin/auth/user/index/"</script>')


# 管理组添加
@permission_required('auth.add_user',raise_exception=True)
def groupadd(request):
    if request.method == 'POST':
        # 接收数据
        name = request.POST.get('name')

        # 创建组
        ob = Group(name=name)
        ob.save()

        # 给组分配权限
        ps = request.POST.getlist('ps', None)
        if ps:
            # 获取选择的权限对象
            prms = Permission.objects.filter(id__in=ps)
            ob.permissions.set(prms)

        return HttpResponse('<script>location.href="/myadmin/auth/group/index/"</script>')
    else:
        # 获取所有的权限
        obs = Permission.objects.exclude(name__istartswith='Can')

        # 分配数据
        context = {'prmslist': obs}

        return render(request, 'myadmin/auth/groupadd.html', context)


# 管理组列表
@permission_required('auth.add_user',raise_exception=True)
def groupindex(request):
    # 获取所有的组对象
    obs = Group.objects.all()

    context = {'grouplist': obs}

    return render(request, 'myadmin/auth/groupindex.html', context)


# 管理组修改页
@permission_required('auth.add_user',raise_exception=True)
def groupedit(request):
    gid = request.GET['gid']

    ob = Group.objects.get(id=gid)

    ps = Permission.objects.exclude(id__in=ob.permissions.all()).exclude(name__istartswith='Can')

    return render(request,'myadmin/auth/groupedit.html',{'data':ob,'ps':ps})


# 管理组修改执行
@permission_required('auth.add_user',raise_exception=True)
def groupupdate(request):
    # 获取要修改管理组的id
    gid = request.POST['gid']
    # 获取对象
    ob = Group.objects.get(id=gid)

    ob.name = request.POST['name']

    ob.permissions.clear()

    gs = request.POST.getlist('gs', None)
    if gs:
        ob.permissions.set(Permission.objects.filter(id__in=gs))

    return HttpResponse('<script>location.href="/myadmin/auth/group/index/"</script>')

