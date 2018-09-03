from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from myadmin.models import Slideshow
from .UserViews import uploads

import os
from web.settings import BASE_DIR


# 轮播图列表页
def index(request):
    ob = Slideshow.objects.all()

    return render(request, 'myadmin/slideshow/index.html', {'data': ob})


# 轮播图添加
def add(request):
    if request.method == 'POST':
        try:
            data = request.POST.dict()
            data.pop('csrfmiddlewaretoken')

            file = request.FILES.get('pic')

            if file:
                data['pic'] = uploads(file)
            else:
                data.pop('pic')

            ob = Slideshow.objects.create(**data)

            return HttpResponse('<script>alert("轮播图添加成功");location.href="/myadmin/slidesshow/index/"</script>')
        except:
            return HttpResponse('<script>alert("轮播图添加失败");history.back(-1);</script>')
    else:
        return render(request, 'myadmin/slideshow/add.html')


# 轮播图编辑页
def edit(request, sid):
    ob = Slideshow.objects.get(id=sid)
    cont = {'data': ob}
    return render(request, 'myadmin/slideshow/edit.html', cont)


# 轮播图执行编辑
def update(request):
    try:
        ob = Slideshow.objects.get(id=request.POST['uid'])
        ob.name = request.POST['name']
        ob.status = request.POST['status']

        file = request.FILES.get('pic', None)

        pic = ob.pic
        if not file:
            ob.pic = pic
        else:
            os.remove(BASE_DIR + ob.pic)
            ob.pic = uploads(file)

        ob.save()
        return HttpResponse('<script>alert("轮播图编辑成功");location.href="/myadmin/slidesshow/index/"</script>')
    except:
        return HttpResponse('<script>alert("轮播图编辑失败");history.back(-1);</script>')


# 轮播图删除
def delete(request, id):
    ob = Slideshow.objects.get(id=id)
    ob.delete()
    return HttpResponse('<script>alert("轮播图删除成功");location.href="/myadmin/slidesshow/index/"</script>')


def status(request):
    if request.is_ajax():
        try:
            ob = Slideshow.objects.get(id=request.GET['sid'])

            ob.status = request.GET['status']

            ob.save()

            return JsonResponse({'code': 0, 'msg': '状态修改成功'})
        except:
            return JsonResponse({'code': 1, 'msg': '状态修改失败'})
    return JsonResponse({'error': 4, 'msg': '请求错误'})
