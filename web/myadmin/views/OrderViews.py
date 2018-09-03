from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from myadmin.models import Goods, Order,OrderInfo,Users
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required


# 订单列表页
@permission_required('myadmin.show_order',raise_exception=True)
def index(request):
    # 获取所有订单
    data = Order.objects.all().order_by('-addtime')

    types = request.GET.get('types')
    keywords = request.GET.get('keywords')
    if types == 'oid':
        data = data.filter(id__contains=keywords).order_by('-addtime')

    if types == 'username':
        user = Users.objects.filter(username__contains=keywords)
        data = Order.objects.filter(uid__in=user).order_by('-addtime')

    if types == 'static':
        if keywords == '未支付':
            data = data.filter(status=0).order_by('-addtime')
        elif keywords == '已支付':
            data = data.filter(status=1).order_by('-addtime')
        elif keywords == '已发货':
            data = data.filter(status=2).order_by('-addtime')
        elif keywords == '已收货':
            data = data.filter(status=3).order_by('-addtime')
        elif keywords == '已取消':
            data = data.filter(status=4).order_by('-addtime')


    page = Paginator(data,5)
    # 获取当前页码数
    p = request.GET.get('p',1)
    # 当前页的数据
    data = page.page(p)

    return render(request, 'myadmin/orders/index.html', {'data':data})

# 订单详情页
@permission_required('myadmin.show_order',raise_exception=True)
def ordersinfo(request):
    oid = request.GET['oid']
    ob = Order.objects.get(id=oid)
    data = OrderInfo.objects.filter(orderid=ob).values()
    for i in data:
        goods = Goods.objects.get(id=i['gid_id'])
        i['goodsid'] = goods.id
        i['goodsname'] = goods.name
        i['goodspic'] = goods.pic
        i['goodsprice'] = goods.price

    context = {'orderlist':list(data)}
    return JsonResponse(context)

# 修改订单状态
@permission_required('myadmin.update_order',raise_exception=True)
def orderstatus(request):

    if request.is_ajax():
        oid = request.GET['oid']
        ob = Order.objects.get(id=oid)
        ob.status = int(request.GET['status'])
        ob.save()
        return JsonResponse({'error':'0','msg':'修改状态成功'})

    return JsonResponse({'error': '1', 'msg': '请求错误'})