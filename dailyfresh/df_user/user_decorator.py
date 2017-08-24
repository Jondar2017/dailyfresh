# coding:utf-8

from django.http import HttpResponseRedirect


def login(func):
    def login_func(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url', request.get_full_path())
            return red
    return login_func

'''
    http://127.0.0.1:8000/200/?a=100
    request.path: 表示当前路径  -> /200/
    request.get_full_path: 表示完整路径  -> /200/?=100
'''
