from io import BytesIO
import math
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import reverse,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from . import models
from . import utils
from . import cachutils



def index(request):
    # 首页不需改变的直接引用
    articles = cachutils.getAllArticles()
    # 分页  ----第一种方法：手写
    pageNow = int(request.GET.get("pageNow", 1))  # 当前是第几页
    pageSize = int(request.GET.get("pageSize", settings.PAGE_SIZE))   # 一页显示几个
    allCount = len(articles)        # 当前共有多少篇文章
    pageCount = math.ceil(allCount/pageSize)     # 所以文章数量/一页显示几个  向上取整 得到一共有多少页
    #
    page = articles[(pageNow - 1) * pageSize:pageNow * pageSize]   # 从第几个开始取，取几个
    pagerange = range(1, pageCount+1)     # 构造循环器

    # 查到所有文章，按照文章的发布时间倒序排列
    # articles = models.Article.objects.filter(type=1).order_by("-publish_time")


    # print(len(users))
    # print(users)
    # ***********************************************************
    # 查热门文章 安装阅读量倒序排列。进行切片显示8个文章
    h_articles = models.Article.objects.filter(Q(type=1) | Q(type=2)).order_by("-publish_time")
    hot_articles = h_articles.order_by("-count")[0:8]
    # 查所有用户 切片 0:6
    users = models.User.objects.all().order_by("-article_num")[0:6]
    # 置顶文章
    article_top = models.Article.objects.filter(type=2).order_by("-publish_time")

    return render(request, "blog/index.html", {"articles": page,    # 数据库取出来的展示在当前页面的文章
                                               "pagerange": pagerange,    # 一页显示的循环几次
                                               "pageNow": pageNow,  # 当前是第几页
                                               "pageSize": pageSize,    # 一页显示几个
                                               "allCount": allCount,    # 当前一共有多少个文章
                                               "pageCount": pageCount,  # 当前一共有多少页
                                               "hot_articles": hot_articles, "users": users, "article_top": article_top})
    # ***********************************************************

def ok(request):
    return render(request, "blog/ok.html", {})



def user_add(request):
    if request.method == "GET":
        return render(request, 'blog/user_add.html', {})
    if request.method == "POST":
        try:
            username = request.POST['username'].strip()
            password = request.POST['password'].strip()
            password2 = request.POST['password2'].strip()
            # name = request.POST['name'].strip()
            # age = request.POST['age'].strip()
            email = request.POST['email']

            # 获取到用户输入的验证码
            code = request.POST['code']
            # 获取当前的code
            mycode = request.session['code']
            # 判断用户输出的验证码和生成的验证码是否相等
            if code.upper() != mycode.upper() :
                return render(request, 'blog/user_add.html', {"msg": "验证码输入有误，请重新输入注册"})

            # 删除session的验证码
            del request.session['code']

            if len(username) < 1:
                return render(request, 'blog/user_add.html', {"msg": "用户名不能为空"})
            if len(username) > 50:
                return render(request, 'blog/user_add.html', {"msg": "用户名过长"})
            if len(models.User.objects.filter(username=username)):
                return render(request, 'blog/user_add.html', {"msg": "用户名已存在"})

            if len(password) < 6:
                return render(request, 'blog/user_add.html', {"msg": "密码不能小于6位"})
            if password != password2 :
                return render(request, 'blog/user_add.html', {"msg": "两次密码输入不一致"})
            # if int(age) < 0:
            #     return render(request, 'blog/user_add.html', {"msg": "年龄不合法"})
            # if int(age) > 0:
            #     return render(request, 'blog/user_add.html', {"msg": "年龄不合法"})
            # if len(name) < 1:
            #     return render(request, 'blog/user_add.html', {"msg": "姓名不合法"})
            # if len(name) > 10:
            #     return render(request, 'blog/user_add.html', {"msg": "姓名不合法"})


            password = utils.hmac_md5(password)
            user = models.User(username=username, password=password, email=email)
            user.save()
            print("11111")
            # return HttpResponseRedirect("/blog/ok")
            return render(request, "blog/ok.html", {})
        except:
            return render(request, '/blog/user_login.html', {"msg": "很抱歉，注册失败！"})

@utils.require_login
def user_list(request):
    users = models.User.objects.all()
    print(users)
    return render(request, 'blog/user_list.html', {"users": users})


@utils.require_login
def user_info(request, u_id):
    user = models.User.objects.get(pk=u_id)
    print(user)
    return render(request, "blog/user_info.html", {"user": user})


@utils.require_login
def del_user(request,u_id):
    user = models.User.objects.get(pk=u_id)
    article = models.Article.objects.get(author_id =u_id)
    # article.type = 0
    # article.save()
    article.delete()
    print(user)
    user.delete()
    return HttpResponseRedirect("/blog/user_list")


@utils.require_login
def update_user(request, u_id):
    user = models.User.objects.get(id=u_id)
    if request.method == "GET":
        return render(request, "blog/update_user.html", {"user": user})
    if request.method == "POST":
        username = request.POST['username']
        age = request.POST['age']
        email = request.POST['email']
        self_info = request.POST['self_info']

        user.username = username
        user.age = age
        user.email = email
        user.self_info = self_info
        print("111")
        user.save()
        print("222")

        return redirect("/blog/user_info/" + str(u_id) + "/")


@utils.require_login
def update_user_header(request, u_id):
    print("开始执行函数")
    user = models.User.objects.get(id=u_id)
    print("获取到用户了")
    header = request.FILES.get('header', 'static/images/headers/default.png')
    print("获取到头像了")
    print(header)
    user.header = header
    user.save()
    print("保存了")
    print(header)
    request.session["LoginUser"] = user
    print("更新了session")
    return redirect("/blog/user_info/" + str(u_id) + "/")


def user_login(request):
    if request.method == "GET":
        return render(request, 'blog/user_login.html', {"msg": "认真填写哟~"})
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username + password)

        # 获取到用户输入的验证码
        code1 = request.POST['code']
        # 获取当前的code
        mycode1 = request.session['code']
        # 判断用户输出的验证码和生成的验证码是否相等
        if code1.upper() != mycode1.upper():
            return render(request, 'blog/user_login.html', {"msg": "验证码输入有误，请重新登录"})

        # 删除session的验证码
        del request.session['code']

        password = utils.hmac_md5(password)

        try:
            user = models.User.objects.get(username=username, password=password)
            # filter 用len(user)判断长度是否登录成功
            print("登录成功")
            request.session["LoginUser"] = user
            return redirect(reverse("blog:main"))
            # return reverse("blog:index")

        except:
            return render(request, "blog/user_login.html", {"msg": "账号或密码错误，请重新登录"})

        # 用filter 查询，用len()判断多少个
        # print("1")
        # user = models.User.objects.filter(username=username, password=password)
        # print("2")
        # print(user)
        # if len(user) > 0:
        #     return render(request, 'blog/index.html', {})
        # else:
        #     return render(request, 'blog/user_login.html', {})

# 文章


@utils.require_login
def add_article(request):
    if request.method == 'GET':
        return render(request, "blog/add_article.html", {})

    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        note = request.POST['note']
        author = request.session['LoginUser']
        feilei = request.POST['feilei']
        if len(note) < 1:
            print("a")
            note = utils.clear_html(content)
            note = note[:80]
            print("========")
            print(note)
            print("==============")

        # return
        print(title, content, note, author, feilei)
        try:
            # headers = request.FILES.get('headers', 'static/images/headers/default.png')
            image = request.FILES.get('image')
            print("****")
            print(image)
            print("*********")
            articles = models.Article.objects.filter(Q(author_id=author.id) & Q(Q(type=1) | Q(type=2)))
            article_num = len(articles)
            article_num += 1

            article = models.Article(title=title, content= content, note= note, author= author, image=image, feilei=feilei)
            article.save()

            user = models.User.objects.get(id=author.id)
            user.article_num = article_num
            print(article_num)
            user.save()


            # 添加文章保存缓存一下下
            cachutils.getAllArticles(ischange=True)

            # return render(request, "blog/index.html", {})
            return redirect(reverse("blog:index"))
            # return JsonResponse({"msg":"成功", "success": True})
        except:
            articles = models.Article.objects.filter(Q(author_id=author.id) & Q(Q(type=1) | Q(type=2)))
            article_num = len(articles)
            article_num += 1
            return
            article = models.Article(title=title, content=content, note=note, author=author, feilei=feilei)
            article.save()
            user = models.User.objects.get(id=author.id)
            user.article_num = article_num
            print(article_num)
            user.save()


            # return render(request, "blog/index.html", {})
            return redirect(reverse("blog:index"))


@utils.require_login
def user_logout(request):
    try:
        del request.session['LoginUser']
    finally:
        return redirect(reverse("blog:index"))


@utils.require_login
def update_self(request):
    u = request.session['LoginUser']
    print(u, u.id)
    self_user = models.User.objects.get(id=u.id)
    if request.method == 'GET':
        return render(request, "blog/update_self.html", {"self_user": self_user, "class":"active", "cls": "tab-pane fade in active", "cls2":"tab-pane fade"})
    elif request.method == 'POST':
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']
        print(old_password, new_password1, new_password2)

        if old_password.strip() != self_user.password:
            return render(request, "blog/update_self.html", {"self_user": self_user, "class2":"active", "cls2": "tab-pane fade in active", "cls":"tab-pane fade", "msg":"输入的当前密码有误！"})
        if len(new_password1.strip()) < 6 :
            return render(request, "blog/update_self.html",{"self_user": self_user, "class2": "active", "cls2": "tab-pane fade in active", "cls": "tab-pane fade", "msg": "新密码小于6位！"})
        if new_password1.strip() != new_password2.strip() :
            return render(request, "blog/update_self.html",{"self_user": self_user, "class2": "active", "cls2": "tab-pane fade in active", "cls": "tab-pane fade", "msg": "两次输入的新密码不相等！"})

        self_user.password = new_password1
        self_user.save()

        try:
            del request.session['LoginUser']
        finally:
            return render(request, "blog/user_login.html", {"msg":"修改密码成功！！要重新登录哦~"})



def code(request):
    img, code = utils.create_code()
    # 首先需要将code 保存到session 中
    request.session['code'] = code
    # 返会图片
    file = BytesIO()
    img.save(file, 'PNG')

    return HttpResponse(file.getvalue(), "image/png")


def show_article(request):
    articles = models.Article.objects.all()
    print(articles)
    return render(request, "blog/index.html", {"articles": articles})


def article_content(request, a_id):
    article = models.Article.objects.get(id=a_id)
    # print(article)
    article.count +=1
    article.save()
    return render(request, "blog/article_content.html", {"article": article})


@utils.require_login
def article_list(request):
    articles = models.Article.objects.filter(Q(type=1) | Q(type=2))
    print(articles)
    return render(request, "blog/article_list.html", {"articles": articles})


@utils.require_login
def del_article_list(request):
    articles = models.Article.objects.filter(type=0)
    print(articles)
    return render(request, "blog/article_list.html", {"articles": articles})


@utils.require_login
def article_top(request, a_id):
    article = models.Article.objects.get(id=a_id)
    print(article.title)
    article.type = 2
    print("11111111")
    print(article.type)
    article.save()
    cachutils.getAllArticles(ischange=True)
    print(article)
    return HttpResponseRedirect("/blog/article_list/")


@utils.require_login
def article_del_top(request, a_id):
    article = models.Article.objects.get(id=a_id)
    print(article.title)
    article.type = 1
    print("2222222222")
    article.save()
    print(article.type)
    print(article)
    return HttpResponseRedirect("/blog/article_list/")


@utils.require_login
def article_del_res(request, a_id):
    article = models.Article.objects.get(id=a_id)
    print(article.title)
    article.type = 1
    print("2222222222")
    article.save()
    cachutils.getAllArticles(ischange=True)
    print(article.type)
    print(article)
    return HttpResponseRedirect("/blog/article_list/")


@utils.require_login
def del_article(request, a_id):
    u = request.session['LoginUser']
    article = models.Article.objects.get(id=a_id)
    print(article)
    article.type = 0
    article.save()
    # 重新缓存一下
    cachutils.getAllArticles(ischange=True)

    user = models.User.objects.get(id=article.author_id)
    user.article_num -= 1
    user.save()

    # article.delete()
    # TODO
    # 缓存一下
    cachutils.getAllArticles(ischange=True)


    if u.type == 0:
        return HttpResponseRedirect("/blog/main/")
    elif u.type == 1:
        return HttpResponseRedirect("/blog/article_list/")


@utils.require_login
def update_article(request, a_id):
    article = models.Article.objects.get(id=a_id)
    if request.method == 'GET':
        print(article)
        return render(request, "blog/update_article.html", {"article": article})
    elif request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        note = request.POST['note']
        feilei = request.POST['feilei']
        # author = request.session['LoginUser']
        print(title, content, note, feilei)

        article.title = title
        article.content = content
        article.note = note
        article.feilei = feilei
        # article.author = author
        article.save()
        # 缓存一下
        cachutils.getAllArticles(ischange=True)

        return redirect("/blog/article_content/" + str(a_id) + "/")


@utils.require_login
def main(request):
    try:
        u = request.session['LoginUser']
        print(u.username)

        articles = models.Article.objects.filter(Q(author_id = u.id) & Q(Q(type=1) | Q(type=2)))
        print("****-")
        print(len(articles))
        a_num = len(articles)
        print("****-")

        return render(request, "blog/main.html", {"articles": articles, "a_num":a_num, "u":u})
    except:
        return render(request, 'blog/user_login.html', {"msg": "要先登录，才能查看自己哦~"})



def user(request, u_id):
    # articles = models.Article.objects.filter(Q(author_id=u_id) & Q(Q(type=1) | Q(type=2)))
    articles = models.Article.objects.filter(Q(author_id=u_id) & Q(Q(type=1) | Q(type=2)))
    # articles = models.Article.objects.filter(Q(type='2') & Q(author_id=u_id))
    # articles = models.Article.objects.filter(Q(type=1) | Q(type=2))
    u = models.User.objects.get(id=u_id)
    print(articles, u)
    a_num = len(articles)
    print(a_num)
    return render(request, "blog/user.html", {"articles": articles, "u": u})


def yuanchuang(request):
    articles = models.Article.objects.filter(Q(feilei=2) & Q(Q(type=1) | Q(type=2))).order_by("-publish_time")
    print(articles)
    hot_articles = articles.order_by("-count")[0:9]
    return render(request, 'blog/feilei.html', {"articles": articles, "hot_articles":hot_articles})


def banyun(request):
    articles = models.Article.objects.filter(Q(feilei=1) & Q(Q(type=1) | Q(type=2))).order_by("-publish_time")
    print(articles)
    hot_articles = articles.order_by("-count")[0:9]
    return render(request, 'blog/feilei.html', {"articles": articles, "hot_articles":hot_articles})


def other(request):
    articles = models.Article.objects.filter(Q(feilei=3) & Q(Q(type=1) | Q(type=2))).order_by("-publish_time")
    print(articles)
    hot_articles = articles.order_by("-count")[0:9]
    return render(request, 'blog/feilei.html', {"articles": articles, "hot_articles":hot_articles})


def checkusername(request, uname):
    user = models.User.objects.filter(username = uname)
    print(user)
    print(len(user))
    if len(user) > 0:
        return JsonResponse({"msg":"该用户名已存在,请重新输入","success":False})
    else:
        return JsonResponse({"msg":"该用户可用！", "success":True})
