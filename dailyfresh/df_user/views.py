# coding:utf-8

from django.shortcuts import render, redirect
from hashlib import sha1
from . models import *
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from df_goods.models import GoodsInfo
from df_order.models import OrderDetailInfo, OrderInfo
from django.core.paginator import Paginator
import user_decorator


def register(request):
    context = {'title': '注册'}
    return render(request, 'df_user/register.html', context)


def register_handle(request):
    uname = request.POST['user_name']
    upwd1 = request.POST['pwd']
    upwd2 = request.POST['cpwd']
    uemail = request.POST['email']

    # 判断两次密码是否一致
    if upwd1 != upwd2:
        return redirect('/user/register/')
    # 对密码进行加密
    s1 = sha1()
    s1.update(upwd1)
    upwd3 = s1.hexdigest()
    # 注册
    userinfo = UserInfo()
    userinfo.uname = uname
    userinfo.upwd = upwd3
    userinfo.uemail = uemail
    userinfo.save()
    # 注册成功之后转到登录页面
    return redirect('/user/login/')


def register_exit(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    if count > 0:
        return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '登录', 'error_user': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    post = request.POST
    username = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    # 从数据库中获取数据
    users = UserInfo.objects.filter(uname=username)
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('url', '/goods/index/')
            print url
            red = HttpResponseRedirect(url)
            if jizhu != 0:
                red.set_cookie('uname', username)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['uname'] = username
            return red
        else:
            context = {'title': '登录', 'error_user': 0, 'error_pwd': 1, 'uname': username, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '登录', 'error_user': 1, 'error_pwd': 0, 'uname': username, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def logout(request):
    response = HttpResponseRedirect('/user/login/')
    request.session.flush()
    response.delete_cookie('goods_ids')
    return response


@user_decorator.login
def info(request):
    uname = request.session.get('uname')
    user_id = request.session.get('user_id')
    uemail = UserInfo.objects.filter(id=user_id)[0].uemail
    goods_ids = request.COOKIES.get('goods_ids', '')
    print goods_ids
    if goods_ids != '':
        goods_ids_list = goods_ids.split(',')
        goods_list = []
        for goods_id in goods_ids_list:
            goods = GoodsInfo.objects.get(id=int(goods_id))
            goods_list.append(goods)
    else:
        goods_list = []

    context = {'title': '用户中心', 'uname': uname, 'uemail': uemail, 'page_num': 1, 'goods_list': goods_list}
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request, pindex=1):
    uid = request.session['user_id']
    order_list = OrderInfo.objects.filter(user_id=int(uid))
    paginator = Paginator(order_list, 2)
    page = paginator.page(int(pindex))
    context = {'title': '用户中心', 'page_num': 1, 'order_list': order_list, 'paginator': paginator, 'page': page}
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def site(request):
    user_id = request.session.get('user_id')
    user = UserInfo.objects.get(id=user_id)
    if request.method == 'POST':
        post = request.POST
        user.ushow = post.get('shou')
        user.uadress = post.get('address')
        user.upostcode = post.get('postcode')
        user.uphone = post.get('phone')
        user.save()
    context = {'title': '用户中心', 'user': user, 'page_num': 1}
    return render(request, 'df_user/user_center_site.html', context)
