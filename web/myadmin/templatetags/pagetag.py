from django import template
from django.utils.html import format_html

register = template.Library()

# 自定义分页
@register.simple_tag
def ShowPages(count,request):

    p = int(request.GET.get('p',1))
    res = request.GET.dict()
    kws = ''
    for k,v in res.items():
        if k != 'p':
            kws += '&'+k+'='+v
    # print(kws)

    # 要求最少显示10页
    begin = p - 5
    end = p + 4
    # 判断页码小于5
    if p <= 5:
        begin = 1
        end = 10
    # 判断页码大于count-5
    if p >= count - 5:
        begin = count - 9
        end = count
    # 判断总页数小于10
    if count < 10:
        begin = 1
        end = count

    pages = ''
    # 首页
    pages += '<li><a href="?p=1'+kws+'">首页</a></li>'
    # 上一页
    if p == 1:
        pages += '<li class="am-active"><a href="?p=' + str(p) + kws + '">«</a></li>'
    else:
        pages += '<li><a href="?p=' + str(p-1) + kws + '">«</a></li>'

    for i in range(begin,end+1):
        if p == i:
            pages += '<li class="am-active"><a href="?p='+str(i)+kws+'">'+str(i)+'</a></li>'
        else:
            pages += '<li><a href="?p='+str(i)+kws+'">' + str(i) + '</a></li>'

    # 下一页
    if p == count:
        pages += '<li class="am-active"><a href="?p=' + str(count) + kws + '">»</a></li>'
    else:
        pages += '<li><a href="?p=' + str(p+1) + kws + '">»</a></li>'
    # 尾页
    pages += '<li><a href="?p=' + str(count) + kws + '">尾页</a></li>'

    return format_html(pages)


# 自定义获取标签
@register.simple_tag
def GetNavList():
    from myadmin.models import Types
    from django.core.urlresolvers import reverse
    # 获取所有的二级分类
    navlist = Types.objects.exclude(pid=0)
    s = ''
    for i in navlist:
        s += '''
                <li class="layout-header-nav-item">
                  <a href="{u}" class="layout-header-nav-link">{name}</a>
                </li>
            '''.format(name=i.name, u=reverse('home_list', args=(i.id,)))
    return format_html(s)

