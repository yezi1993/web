from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from django.core.paginator import Paginator
# Create your views here.

from .TypesViews import GetTypes
from .UserViews import uploads

from myadmin.models import Goods, Types

import os
from web.settings import BASE_DIR
from django.contrib.auth.decorators import permission_required

# 商品列表
@permission_required('myadmin.show_goods',raise_exception=True)
def index(request):
    # 获取所有的商品
    obs = Goods.objects.all()
    types = request.GET.get('types', None)
    keywords = request.GET.get('keywords', None)
    # 判断是否右搜索条件
    if types:
        if types == 'all':
            # Q对象
            from django.db.models import Q
            obs = Goods.objects.filter(Q(name__icontains=keywords) | Q(price__contains=keywords))
        elif types == 'name' or types == 'price':
            kvs = {types + '__icontains': keywords}
            obs = obs.filter(**kvs)
        elif types == 'name':
            # 按分类名搜索
            # 查看分类名包含
            ts = Types.objects.filter(name__icontains=keywords)
            # 获取当前商品的tid符合ts的
            obs = Goods.objects.filter(tid__in=ts)

    # 导入分页类
    page = Paginator(obs, 10)
    # 获取当前的页码数
    p = request.GET.get('p', 1)
    # 当前页数据
    data = page.page(p)

    # 分配数据
    context = {'goodslist': data}

    # 加载模板
    return render(request, 'myadmin/goods/index.html', context)


# 商品添加
@permission_required('myadmin.insert_goods',raise_exception=True)
def add(request):
    if request.method == 'GET':
        # 调用封装好的函数,获取所有的分类
        context = {'typeslist': GetTypes()}

        # 加载模板,.分配数据
        return render(request, 'myadmin/goods/add.html', context)
    else:
        try:

            # 判断是有文件上传
            myfile = request.FILES.get('face', None)
            if not myfile:
                return HttpResponse('<script>alert("请选择商品图片上传");history.back(-1);</script>')

            # 接收数据
            data = request.POST.dict()
            data.pop('csrfmiddlewaretoken')
            # 调用函数进行文件上传
            data['pic'] = uploads(myfile)
            data['tid'] = Types.objects.get(id=data['tid'])

            # 执行数据添加
            ob = Goods.objects.create(**data)

            return HttpResponse('<script>alert("商品添加成功");location.href="/myadmin/goods/index/"</script>')
        except:
            return HttpResponse('<script>alert("商品添加失败");history.back(-1);</script>')

# 商品编辑页
@permission_required('myadmin.update_goods',raise_exception=True)
def edit(request,uid):
    if request.method == 'GET':
        obs = Goods.objects.get(id=uid)
        context = {'data':obs}

        context['typeslist'] = GetTypes()
        return render(request, 'myadmin/goods/edit.html',context)

# 执行商品编辑
@permission_required('myadmin.update_goods',raise_exception=True)
def update(request):

    if request.method == 'POST':
        try:
            ob = Goods.objects.get(id=request.POST['uid'])

            ob.name = request.POST['name']
            ob.store = request.POST['store']
            ob.info = request.POST['info']
            ob.tid = Types.objects.get(id=request.POST['tid'])
            file = request.FILES.get('pic',None)
            print(ob.pic)
            pic = ob.pic
            if not file:
                ob.pic = pic
            else:
                os.remove(BASE_DIR + ob.pic)
                ob.pic = uploads(file)

            ob.save()
            return HttpResponse('<script>alert("商品编辑成功");location.href="/myadmin/goods/index/"</script>')
        except:
            return HttpResponse('<script>alert("商品添加失败");history.back(-1);</script>')

    else:
        return HttpResponse('请求错误')

# 修改商品状态
@permission_required('myadmin.remove_goods',raise_exception=True)
def delete(request):

        if request.is_ajax():
            try:
                ob = Goods.objects.get(id=request.GET['uid'])

                ob.status = request.GET['status']

                ob.save()

                return JsonResponse({'code': 0, 'msg': '状态修改成功'})
            except:
                return JsonResponse({'code': 1, 'msg': '状态修改失败'})
        return JsonResponse({'error': 4, 'msg': '请求错误'})

def rexiao(request):
    if request.is_ajax():
        try:
            ob = Goods.objects.get(id=request.GET['uid'])

            ob.rexiao = request.GET['rexiao']

            ob.save()

            return JsonResponse({'code': 0, 'msg': '状态修改成功'})
        except:
            return JsonResponse({'code': 1, 'msg': '状态修改失败'})
    return JsonResponse({'error': 4, 'msg': '请求错误'})


