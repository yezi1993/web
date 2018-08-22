from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from myadmin.models import Users

import os
from web.settings import BASE_DIR
# 用户列表页
def index(request):
    data = Users.objects.all()

    return render(request,'myadmin/users/index.html',{'data':data})

# 用户添加
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
def delete(request):
    # 接受uid
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



# 用户编辑
def edit(request,uid):
    ob = Users.objects.get(id=uid)
    cont = {'data':ob}
    return render(request,'myadmin/users/edit.html',cont)


# 用户编辑处理
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



    return HttpResponse('222')

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