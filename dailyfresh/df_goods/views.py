# coding:utf-8
from django.shortcuts import render
from . models import *
from django.core.paginator import *
from df_user import user_decorator



def index(request):
    typeinfo = TypeInfo.objects.all()
    type0 = typeinfo[0].goodsinfo_set.order_by('-id')[0:3]
    type01 = typeinfo[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = typeinfo[1].goodsinfo_set.order_by('-id')[0:3]
    type11 = typeinfo[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typeinfo[2].goodsinfo_set.order_by('-id')[0:3]
    type21 = typeinfo[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typeinfo[3].goodsinfo_set.order_by('-id')[0:3]
    type31 = typeinfo[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typeinfo[4].goodsinfo_set.order_by('-id')[0:3]
    type41 = typeinfo[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typeinfo[5].goodsinfo_set.order_by('-id')[0:3]
    type51 = typeinfo[5].goodsinfo_set.order_by('-gclick')[0:4]

    context = {'title': '首页', 'guest_cart': 1,
               'type0': type0, 'type01': type01,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type21': type21,
               'type3': type3, 'type31': type31,
               'type4': type4, 'type41': type41,
               'type5': type5, 'type51': type51,
               }
    return render(request, 'df_goods/index.html', context)


def list(request, tid, pindex, sort):
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':  # 默认,最新
        goods_list = typeinfo.goodsinfo_set.order_by('-id')
    elif sort == '2':  # 价格
        goods_list = typeinfo.goodsinfo_set.order_by('-gprice')
    elif sort == '3':  # 人气
        goods_list = typeinfo.goodsinfo_set.order_by('-gclick')
    paginator = Paginator(goods_list, 2)
    page = paginator.page(pindex)
    context = {'title': '商品列表', 'guest_cart': 1,
               'news': news,
               'typeinfo': typeinfo,
               'sort': sort,
               'paginator': paginator,
               'page': page,
               }
    return render(request, 'df_goods/list.html', context)


def detail(request, pindex):
    goods = GoodsInfo.objects.get(pk=int(pindex))
    goods.gclick += 1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {'title': '商品详情', 'guest_cart': 1,
               'goods': goods,
               'news': news,
               }

    response = render(request, 'df_goods/detail.html', context)

    # 构建最近浏览商品，供用户中心使用
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = '%d' % goods.id
    if goods_ids != '':  # 判断是否有浏览记录
        goods_ids1 = goods_ids.split(',')  # 拆分成一个数组
        if goods_ids1.count(goods_id) >= 1:  # 如果商品已经被记录了,则删除
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0, goods_id)  # 添加到第一个
        if len(goods_ids1) > 5:  # 如果列表中有超过6条记录,则删除最后一条
            goods_ids1.pop()
        goods_ids = ','.join(goods_ids1)  # 拼接为字符串
    else:
        goods_ids = goods_id  # 如果没有浏览记录则直接加
    response.set_cookie('goods_ids', goods_ids)

    return response

from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['title'] = '搜索'
        context['guest_cart'] = 1
        # context['cart_count'] = cart_count(self.request)
        return context
