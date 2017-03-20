#!/usr/bin/env python
# coding: utf-8
# zdy.py
'''
Squid+站大爷搭建代理IP池
Author: Nathan
Blog: www.xnathan.com
Github: github.com/xNathan
'''
from gevent import monkey
monkey.patch_all()

import os
import time
import requests
from gevent.pool import Pool

# Squid的配置文件语法
# 将请求转发到父代理
PEER_CONF = "cache_peer %s parent %s 0 no-query weighted-round-robin weight=1 connect-fail-limit=2 allow-miss max-conn=5\n"

# 可用代理
GOOD_PROXIES = []

pool = Pool(50)

def check_proxy(proxy):
    """验证代理是否可用
    :param proxy list:[ip, port]"""
    global GOOD_PROXIES
    ip, port = proxy
    _proxies ={
        'http': '{}:{}'.format(ip, port)
    }
    try:
        res = requests.get(
            'http://1212.ip138.com/ic.asp', proxies=_proxies, timeout=10)
        assert ip in res.content
        print '[GOOD] - {}:{}'.format(ip, port)
        GOOD_PROXIES.append(proxy)
    except Exception, e:
        print '[BAD] - {}:{}'.format(ip, port)


def update_conf():
    with open('/etc/squid/squid.conf.original', 'r') as F:
        squid_conf = F.readlines()
    squid_conf.append('\n# Cache peer config\n')
    for proxy in GOOD_PROXIES:
        squid_conf.append(PEER_CONF % (proxy[0], proxy[1]))
    with open('/etc/squid/squid.conf', 'w') as F:
        F.writelines(squid_conf)


def get_proxy():
    global GOOD_PROXIES
    GOOD_PROXIES = []
    # 1. 获取代理IP资源
    api_url = 'http://s.zdaye.com/?api=YOUR_API&count=100&fitter=1&px=2'
    res = requests.get(api_url).content
    if len(res) == 0:
        print 'no data'
    elif 'bad' in res:
        print 'bad request'
    else:
        print 'get all proxies'
        proxies = []
        for line in res.split():
            proxies.append(line.strip().split(':'))
        pool.map(check_proxy, proxies)
        pool.join()
        # 2. 写入Squid配置文件
        update_conf()
        # 3. 重新加载配置文件
        os.system('squid -k reconfigure')
        print 'done'


def main():
    start = time.time()
    while True:
        # 每30秒获取一批新IP
        if time.time() - start >= 30:
            get_proxy()
            start = time.time()
        time.sleep(5)


if __name__ == '__main__':
    main()
