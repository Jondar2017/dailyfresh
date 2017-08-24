# coding:utf-8
from django.shortcuts import render, redirect
from .models import *
from df_cart.models import *
from df_user.models import *
from df_user import user_decorator
from django.db import transaction
from datetime import datetime
from decimal import Decimal



@user_decorator.login
def order(request):

    uid = request.session.get('user_id', '')
    # 求当前的用户
    user = UserInfo.objects.get(pk=int(uid))
    get = request.GET
    cart_ids = get.getlist('cart_id', '')
    # 求出购物车中的商品
    cids = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(pk__in=cids)
    context = {'title': '提交订单', 'page_num': 1, 'carts': carts, 'user': user}
    return render(request, 'df_order/place_order.html', context)


# @transaction.automic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    # 接收购物车编号
    post = request.POST
    cart_ids = post.getlist('cart_id', '')
    print cart_ids
    try:
        # 创建订单对象
        order = OrderInfo()
        uid = request.session.get('user_id', '')
        now = datetime.now()
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        print order.oid
        order.ototal = Decimal(post.get('total', ''))
        order.oaddress = post.get('address', '')
        order.save()
        # print order.oaddress

        # 创建订单详情
        for cart_id in cart_ids:
            detail = OrderDetailInfo()
            detail.order = order
            # 查询的购物车信息
            cart = CartInfo.objects.get(id=int(cart_id))
            goods = cart.goods
            # 判断商品库存
            if goods.gstock >= cart.count: # 如果库存大于购买数量
                goods.gstock = goods.gstock - cart.count
                goods.save()
                # 完善订单信息
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()

                # 删除购物车信息
                cart.delete()
            else:  # 如果库存小于购买数量
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
            transaction.commit(tran_id)

    except Exception as e:
        print "===================%s" % e
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order1/')
