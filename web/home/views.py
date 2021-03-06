from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.hashers import make_password,check_password

from myadmin.models import Users,Types,Goods,Citys,Order,OrderInfo,Address,Slideshow

import os
from web.settings import BASE_DIR

# Create your views here.
# 首页
def index(request):
    # 获取顶级分类
    data = Types.objects.filter(pid=0)

    # 将所有二级分类保存起来
    for i in data:
        i.sub = Types.objects.filter(pid=i.id)
    # 获取所有的商品
    goods = Goods.objects.filter()
    data.goods = goods
    # 查询热销商品
    rexiao = goods.filter(rexiao=1).order_by('-update_time')
    lunbo = Slideshow.objects.filter(status=1)

    cont = {'typeslist':data,'rexiao':rexiao,'lunbo':lunbo}
    return render(request, 'home/index.html',cont)


#  列表
def list(request,tid):
    # 获取分类id
    data = Types.objects.get(id=tid)

    # 判断是不是顶级分类
    if data.pid == 0:
        data.sub = Types.objects.filter(pid=data.id)
        data.goods = Goods.objects.filter(tid__in=data.sub)
    else:
        data.sub = Types.objects.filter(pid=data.pid)
        data.goods = Goods.objects.filter(tid=data.id)

    cont = {'data':data}


    return render(request, 'home/list.html',cont)


#  详情
def info(request,gid):
    data = Goods.objects.get(id=gid)
    data.clicknum += 1
    data.save()

    return render(request, 'home/info.html',{'data':data})


#  注册
def register(request):
    if request.method == 'GET':
        # 返回一个注册 表单页面
        return render(request, 'home/register.html')
    elif request.method == 'POST':
        # 执行注册
        try:

            # 接受数据
            data = request.POST.dict()

            # if Users.objects.filter(phone=data['phone']):
            #     return HttpResponse('<script>alert("手机号已存在，请重新填写");history.back(-1);</script>')
            # 先检测验证码是否正确
            if str(data['vcode']) != str(request.session['code']):
                return HttpResponse('<script>alert("验证码错误");history.back(-1);</script>')

            data.pop('csrfmiddlewaretoken')
            data.pop('vcode')

            # 密码加密
            data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')

            # 创建数据对象
            Users.objects.create(**data)

            return HttpResponse('<script>alert("注册成功，请登录");location.href="/login/"</script>')
        except:
            return HttpResponse('<script>alert("注册失败，请联系管理员");history.back(-1);</script>')


# 登录
def login(request):
    # 获取地址
    nextpath = request.GET.get('nextpath','/')

    if request.method == "GET":
        # 返回一个 登录 页面
        return render(request,'home/login.html')
    elif request.method == 'POST':
        # 执行登录
        # 接受数据
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        try:
            # 先根据手机号获取用户对象
            ob = Users.objects.get(phone=data['phone'])

            # 再比对密码
            if check_password(data['password'], ob.password):
                # 把用户的数据信息,写入session
                request.session['VipUser'] = {'uid': ob.id, 'username': ob.username, 'pic': ob.pic}
                # 成功
                return HttpResponse('<script>alert("欢迎登录商城");location.href="' + nextpath + '"</script>')
        except:
            pass

        return HttpResponse('<script>alert("账号或密码错误");history.back(-1)</script>')


# 退出登录
def logout(request):
    request.session['VipUser'] = ''

    return HttpResponse('<script>alert("退出成功,欢迎下次登录");location.href="/"</script>')


# 发送短信验证码
def sendSMS(request):
    import random
    # 接受手机号
    phone = request.GET.get('phone')

    # 生成验证码
    code = random.randint(11111, 99999)
    # 存储到session中
    request.session['code'] = code

    print(code)

    # 调用方法 发送短信验证
    from dysms import demo_sms_send
    res = demo_sms_send.send(code, phone)

    return HttpResponse(res)

# 购物车添加
def cartadd(request):
    if request.method == 'GET':
        gid = request.GET.get('gid')
        num = int(request.GET.get('num'))
        # 获取session中购物车的数据
        data = request.session.get('cart', {})

        # 判断要加入购物车的商品是否存在
        if data.get(gid):
            # 存在修改商品数量
            data[gid]['num'] += num
        else:
            data[gid] = {'gid': gid, 'num': num}

        # 将配置好的购物车数据，存到session
        request.session['cart'] = data

    return JsonResponse({'error': 0, 'msg': '成功加入购物车！！！'})


# 购物车列表
def cartlist(request):
    try:
        # 获取所有的购物车的商品
        data = request.session['cart']

        for k, v in data.items():
            data[k]['goods'] = Goods.objects.get(id=k)

        return render(request, 'home/cartlist.html', {'data': data})
    except:
        return HttpResponse('<script>alet("请选择商品");location.href="/"</script>')

# 购物车修改
def cartedit(request):
    # 获取 商品id,数量
    gid = request.GET.get('gid')
    num = request.GET.get('num')

    # 在session中获取购物车数据
    data = request.session['cart']

    # 修改商品数量
    data[gid]['num'] = int(num)

    # 把修改好的购物车数据,再放回到session
    request.session['cart'] = data

    return JsonResponse({'error': 0, 'msg': '购物车商品更新成功'})


# 删除购物车里的商品
def cartdelete(request):
    gid = request.GET.get('gid')

    data = request.session['cart']

    data.pop(gid)

    request.session['cart'] = data

    return JsonResponse({'error': '0', 'msg': '商品删除成功'})

# 订单确认
def orderconfirm(request):
    # 接收ids {'8': 1, '3': 2} <class 'dict'>
    ids = eval(request.GET.get('ids'))

    # 准备数据
    data = []
    for k, v in ids.items():
        ob = Goods.objects.get(id=k)
        ob.num = v
        data.append(ob)

    # 获取当前用户的所有收货地址
    adds = Address.objects.filter(uid=request.session['VipUser']['uid'])

    # 分配数据
    context = {'data': data, 'adds': adds}

    # 加载模板
    return render(request, 'home/confirm.html', context)


# 创建订单
def ordercreate(request):
    # 接受ids 已经选择的商品id和数量

    ids = eval(request.POST.get('ids'))

    # 创建订单
    ob = Order()
    ob.uid = Users.objects.get(id=request.session['VipUser']['uid'])
    ob.aid = Address.objects.get(id=request.POST.get('addressid'))
    ob.totalprice = 0
    ob.save()

    # 获取session中的购物车数据
    CartData = request.session['cart']

    # 创建订单详情
    totalprice = 0
    for k, v in ids.items():
        obi = OrderInfo()
        obi.orderid = ob
        g = Goods.objects.get(id=k)
        obi.gid = g
        obi.num = v
        obi.price = g.price
        obi.save()
        # 把已经下单的商品在购物车中删除
        CartData.pop(k)
        totalprice += g.price * v

    # 修改总价
    ob.totalprice = totalprice
    ob.save()

    # 把修改好的购物车数据,重新放入session
    request.session['cart'] = CartData

    return HttpResponse('<script>location.href="/order/buy/?orderid=' + str(ob.id) + '"</script>')


# 订单支付
def orderbuy(request):
    # 接受订单id
    orderid = request.GET.get('orderid')

    print(orderid)

    # 显示支付页面
    # return HttpResponse('orderbuy')
    return HttpResponseRedirect('/my/order/')

# 我的订单
def myorder(request):
    # 获取用户
    uid = request.session['VipUser']['uid']
    ob = Users.objects.get(id=uid)
    data = Order.objects.filter(uid=ob).order_by('-addtime')

    # 分配数据
    context = {'data': data}
    # 加载页面
    return render(request, 'home/myorder.html', context)


# 待发货
def daifahuo(request):
    # 获取用户
    uid = request.session['VipUser']['uid']
    ob = Users.objects.get(id=uid)
    data = Order.objects.filter(uid=ob,status=1).order_by('-addtime')

    return render(request,'home/orders/daifahuo.html',{'data': data})


# 待付款
def daifukuan(request):

    uid = request.session['VipUser']['uid']
    ob = Users.objects.get(id=uid)
    data = Order.objects.filter(uid=ob,status=0).order_by('-addtime')

    return render(request,'home/orders/daifukuan.html',{'data': data})


# 已发货
def yifahuo(request):
    # 获取用户
    uid = request.session['VipUser']['uid']
    ob = Users.objects.get(id=uid)
    data = Order.objects.filter(uid=ob,status=2).order_by('-addtime')

    return render(request,'home/orders/yifahuo.html',{'data': data})


# 个人中心
def mycentre(request):

    ob = Users.objects.get(id=request.session['VipUser']['uid'])
    orderN = Order.objects.filter(uid=ob,status=0).count()
    orderY = Order.objects.filter(uid=ob,status=1).count()

    return render(request,'home/mycentre.html',{'data':ob,'orderN':orderN,'orderY':orderY})


# 编辑个人信息
def useredit(request):

    ob = Users.objects.get(id=request.session['VipUser']['uid'])


    if request.method == 'GET':

        return render(request, 'home/useredit.html',{'data':ob})

    elif request.method == 'POST':
        try:
            ob.username = request.POST['username']
            # # 判断用户是否修改密码
            if request.POST.get('password',None):
                ob.password = make_password(request.POST['password'],None,'pbkdf2_sha256')
            ob.email = request.POST['email']
            ob.phone = request.POST['phone']
            ob.age = request.POST['age']
            ob.sex = request.POST['sex']
            #
            file = request.FILES.get('pic',None)
            # 判断用户是否修改了头像
            if file:

                if ob.pic != '/static/pics/user.gif':
                    os.remove(BASE_DIR+ob.pic)

                ob.pic = uploads(file)
            #
            ob.save()
            return HttpResponse('<script>alert("会员编辑成功");location.href="/my/centre/"</script>')
        except:
            return HttpResponse('<script>alert("会员编辑失败");history.back(-1);</script>')


# 收货地址的添加
def addressinsert(request):
    # 接受数据.
    data = request.POST.dict()
    ids = request.POST.get('ids')
    data.pop('csrfmiddlewaretoken')
    data.pop('ids')

    # 获取用户对象
    data['uid'] = Users.objects.get(id=request.session['VipUser']['uid'])
    # 执行数据的添加
    ob = Address.objects.create(**data)

    # 判断如果当前地址设为默认.那么其它地址都要取消默认
    if ob.isstatus:
        obs = Address.objects.filter(uid=data['uid']).exclude(id=ob.id)
        for x in obs:
            x.isstatus = False
            x.save()

    res = '''
        <script>location.href='/order/confirm/?ids={ids}';</script>
        '''.format(ids=ids)
    return HttpResponse(res)

# 收货地址展示
def addresslist(request):

    ob = Users.objects.get(id=request.session['VipUser']['uid'])

    data = Address.objects.filter(uid=ob)

    return render(request,'home/address/list.html',{'data':data})


# 收货地址编辑
def addressedit(request):
        aid = request.GET['aid']
        data = Address.objects.get(id=aid)
        return render(request,'home/address/edit.html',{'data':data})


# 执行收货地址编辑
def addressupdate(request):

    if request.method == 'POST':
        aid = request.POST['aid']
        ob = Address.objects.get(id=aid)
        try:
            ob.aname = request.POST['aname']
            ob.ads = request.POST['ads']
            ob.aphone = request.POST['aphone']
            ob.atags = request.POST['atags']
            if request.POST['isstatus'] == '0':
                ob.isstatus = True
                uobj = Users.objects.get(id=request.session['VipUser']['uid'])
                obs = Address.objects.filter(uid=uobj).exclude(id=ob.id)
                for x in obs:
                    x.isstatus = False
                    x.save()
            else:
                ob.isstatus = False

            ob.save()
            return HttpResponse('<script>alert("修改地址成功");location.href="/address/list/"</script>')
        except:

            return HttpResponse('<script>alert("修改地址失败");history.back(-1)</script>')


# 删除收获地址
def addressdel(request):
    # 获取要删除地址的id
    aid = request.GET['aid']
    # 获取对象
    data = Address.objects.get(id=aid)
    data.delete()
    return HttpResponse('<script>alert("删除地址成功");location.href="/address/list/"</script>')



# 设置默认地址
def addressstatus(request):
    if request.is_ajax():
        # 获取要修改的地址id
        aid = request.GET['aid']
        try:
            # 获取对象
            ob = Address.objects.get(id=aid)
            # 修改状态
            ob.isstatus = True
            # 获取当前的用户对象
            uobj = Users.objects.get(id=request.session['VipUser']['uid'])
            # 查找此用户下的其他地址
            obs = Address.objects.filter(uid=uobj).exclude(id=ob.id)
            # 因为默认地址是唯一所以修改其他地址的状态
            for x in obs:
                x.isstatus = False
                x.save()

            ob.save()

            return JsonResponse({'error': '0', 'mgs': '设置默认地址成功'})
        except:
            return JsonResponse({'error': '1', 'mgs': '设置默认地址失败'})


# 图片上传
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
