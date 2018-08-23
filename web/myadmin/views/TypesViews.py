from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from myadmin.models import Types
from django.core.paginator import Paginator

# 获取格式化分类数据
def GetTypes():
    # 获取所有的分类
    obs = Types.objects.extra(select={'paths': 'concat(path,id)'}).order_by('paths')

    for x in obs:
        if x.pid == 0:
            x.pname = '顶级分类'
        else:
            # 获取父级对象的数据
            ob = Types.objects.get(id=x.pid)
            x.pname = ob.name

    # 返回处理号的数据
    return obs

# 分类列表页
def index(request):

    obs = GetTypes()

    cont = {'typeslist':obs}

    return render(request,'myadmin/types/index.html',cont)

# 分类添加
def add(request):

    if request.method == 'GET':

        ob = GetTypes()

        return render(request,'myadmin/types/add.html',{'typeslist':ob})
    elif request.method == 'POST':
        try:
            data = request.POST.dict()
            data.pop('csrfmiddlewaretoken')
            if data['pid'] == '0':
                    data['path'] = '0,'
            else:
                ob = Types.objects.get(id=data['pid'])
                data['path'] = ob.path+data['pid']+','

            ob = Types.objects.create(**data)
            return HttpResponse('<script>alert("分类编辑成功");location.href="/myadmin/types/index/"</script>')
        except:
            return HttpResponse('<script>alert("分类编辑失败");history.back(-1);</script>')


# 分类删除
def delete(request):
    if request.is_ajax():
        ob = Types.objects.get(id=request.GET['uid'])

        res = Types.objects.filter(pid = ob.id)
        if res:
            return JsonResponse({'error': '2', 'mgs': '删除失败，此分类下还有子类不允许删除'})
        else:
            ob.delete()
            return JsonResponse({'error': '0', 'mgs': '分类删除成功'})

    return JsonResponse({'error':'1','mgs':'非法请求'})


# 分类编辑
def edit(request):
    if request.is_ajax():

        ob = Types.objects.get(id = request.GET['tid'])

        ob.name = request.GET['name']

        ob.save()

        return JsonResponse({'error': '0', 'mgs': '修改成功'})

    return JsonResponse({'error': '1', 'mgs': '非法请求'})

