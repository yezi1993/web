from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from myadmin.models import Users
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required

import os
from web.settings import BASE_DIR

# 用户列表页
@permission_required('myadmin.show_users',raise_exception=True)
def index(request):

    data = Users.objects.filter()
    # 用户搜索
    types = request.GET.get('types')
    keywords = request.GET.get('keywords')
    if types == 'username':
        data = data.filter(username__contains=keywords)

    if types == 'phone':
        data = data.filter(phone__contains=keywords)

    if types == 'email':
        data = data.filter(email__contains=keywords)

    if types == 'age':
        data = data.filter(age=keywords)

    if types == 'sex':
        if keywords == '男':
            data = data.filter(sex='1')
        elif keywords == '女':
            data = data.filter(sex='0')

    if types == 'status':
        if keywords == '正常':
            data = data.filter(status=1)
        elif keywords == '禁用':
            data = data.filter(status=0)


    # 实例化分页
    page = Paginator(data,5)
    # 获取当前页码数
    p = request.GET.get('p',1)
    # 当前页的数据
    data = page.page(p)


    return render(request,'myadmin/users/index.html',{'data':data})

# 用户添加
@permission_required('myadmin.insert_users',raise_exception=True)
def add(request):
    if request.method == 'GET':

        return render(request, 'myadmin/users/add.html')
    elif request.method == 'POST':

        try:
            data = request.POST.dict()
            data.pop('csrfmiddlewaretoken')
            data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')

            file = request.FILES.get('pic')

            print(file)

            if file:
                data['pic'] = uploads(file)
            else:
                data.pop('pic')

            ob = Users.objects.create(**data)

            return HttpResponse('<script>alert("会员添加成功");location.href="/myadmin/user/index/"</script>')
        except:
            return HttpResponse('<script>alert("会员添加失败");history.back(-1);</script>')

# 用户删除
@permission_required('myadmin.remove_users',raise_exception=True)
def delete(request):
    # 接受uid
    if request.is_ajax():
        uid = request.GET.get('uid')
        # 获取用户对象
        ob = Users.objects.get(id=uid)

        # 判断当前用户是否使用了默认头像
        if ob.pic != '/static/pics/user.gif':

            try:
                # 删除头像
                os.remove(BASE_DIR+ob.pic)
            except:
                data = {'error':1,'msg':'文件删除失败'}
                return JsonResponse(data)

        try:
            # 执行删除
            ob.delete()
            data = {'error':0,'msg':'删除成功'}
        except:
            data = {'error':2,'msg':'数据删除失败'}

        return JsonResponse(data)
    return JsonResponse({'error':4,'msg':'请求错误'})



# 用户编辑
@permission_required('myadmin.update_users',raise_exception=True)
def edit(request,uid):
    ob = Users.objects.get(id=uid)
    cont = {'data':ob}
    return render(request,'myadmin/users/edit.html',cont)


# 用户编辑处理
@permission_required('myadmin.update_users',raise_exception=True)
def update(request):
    try:
        ob = Users.objects.get(id=request.POST['uid'])
        ob.username = request.POST['username']
        # 判断用户是否修改密码
        if request.POST.get('password',None):
            ob.password = make_password(request.POST['password'],None,'pbkdf2_sha256')
        ob.email = request.POST['email']
        ob.phone = request.POST['phone']
        ob.age = request.POST['age']
        ob.sex = request.POST['sex']

        file = request.FILES.get('pic',None)
        # 判断用户是否修改了头像
        if file:

            if ob.pic != '/static/pics/user.gif':
                os.remove(BASE_DIR+ob.pic)

            ob.pic = uploads(file)

        ob.save()
        return HttpResponse('<script>alert("会员编辑成功");location.href="/myadmin/user/index/"</script>')
    except:
        return HttpResponse('<script>alert("会员编辑失败");history.back(-1);</script>')


# 处理文件上传
def uploads(file):
    import random,time

    # 获取文件名
    filename = str(random.randint(11111,99999))+str(time.time())+'.'+file.name.split('.').pop()
    # 打开文件写入
    destination = open(BASE_DIR+"/static/pics/"+filename,"wb+")
    # 分块写入文件
    for chunk in file.chunks():
        destination.write(chunk)

    destination.close()

    return '/static/pics/'+filename

def status(request):

    if request.is_ajax():
        try:
            ob = Users.objects.get(id=request.GET['uid'])

            ob.status = request.GET['status']

            ob.save()

            return JsonResponse({'code':0,'msg':'状态修改成功'})
        except:
            return JsonResponse({'code':1, 'msg': '状态修改失败'})
    return JsonResponse({'error': 4, 'msg': '请求错误'})