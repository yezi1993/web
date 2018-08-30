from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import login,logout
from django.contrib.auth import authenticate

# Create your views here.
# 后台主页
def index(request):

    return render(request,'myadmin/index.html')
    # return HttpResponse('123')

# 后台登录
def myadminlogin(request):
    if request.method == 'POST':
        # 判断验证码
        print('123')
        if request.POST['vcode'].upper() != request.session['verifycode'].upper():
            return HttpResponse('<script>alert("验证码错误！！");history.back(-1);</script>')

        user = authenticate(username=request.POST['username'],password=request.POST['password'])

        if user:
            login(request,user)

            request.session['AdminUser'] = {'username':user.username}

            return HttpResponse('<script>alert("欢迎登录！！");location.href="/myadmin/"</script>')
        else:
            return HttpResponse('<script>alert("用户名或密码错误");history.back(-1);</script>')
    else:

        return render(request, 'myadmin/login.html')


def myadminlogout(request):

    request.session['AdminUser'] = ''
    logout(request)

    return HttpResponse("<script>alert('退出成功');location.href='/myadmin/login/';</script>")



# 验证码
def verifycode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # str1 = '123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('simhei.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')