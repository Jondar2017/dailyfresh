# coding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from df_user import user_decorator
from .models import *


@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=int(uid))
    context = {'title': '购物车', 'page_num': 1, 'carts': carts}
    return render(request, 'df_cart/cart.html', context)


@user_decorator.login
def add(request, gid, count):
    uid = request.session['user_id']
    print uid
    gid = int(gid)
    count = int(count)
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()

    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')


@user_decorator.login
def edit(request, cid, count):
    try:
        cart = CartInfo.objects.get(pk=int(cid))
        count1 = cart.count = int(count)
        cart.save()
        data = {'ok': 0}
    except Exception as e:
        data = {'ok': count1}
    return JsonResponse(data)



def delete(request, cid):
    try:
        cart = CartInfo.objects.get(pk=int(cid))
        cart.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)
