#!/usr/bin/env python
#_*_ coding:utf-8 _*_
# __author__ = "huihui"
# Date: 2017/10/10 0010

import hashlib
from django.shortcuts import HttpResponse
import time
from auto_server import settings


def md5(arg):
    hs = hashlib.md5()
    hs.update(arg.encode('utf-8'))
    return hs.hexdigest()

# redis,Memcache
visited_keys = {
    # "841770f74ef3b7867d90be37c5b4adfc":时间,  10
}

def api_auth(func):
    def inner(request,*args,**kwargs):
        server_float_ctime = time.time()
        auth_header_val = request.META.get('HTTP_AUTH_API')
        # 841770f74ef3b7867d90be37c5b4adfc|1506571253.9937866
        client_md5_str, client_ctime = auth_header_val.split('|', maxsplit=1)
        client_float_ctime = float(client_ctime)

        # 第一关
        if (client_float_ctime + 20) < server_float_ctime:
            return HttpResponse('时间太久了，再去买一个吧')

        # 第二关：
        server_md5_str = md5("%s|%s" % (settings.KEY, client_ctime,))
        if server_md5_str != client_md5_str:
            return HttpResponse('休想')

        # 第三关：
        if visited_keys.get(client_md5_str):
            return HttpResponse('你放弃吧，来晚了')

        visited_keys[client_md5_str] = client_float_ctime
        return func(request,*args,**kwargs)

    return inner

