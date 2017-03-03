#!/usr/bin/env python
# coding: utf-8
# zdy.py
'''
Squid+站大爷搭建代理IP池
Author: Nathan
Blog: www.xnathan.com
Github: github.com/xNathan
'''
import os
import time
import requests
# Squid的配置文件语法
# 将请求转发到父代理
PEER_CONF = "cache_peer %s parent %s 0 no-query weighted-round-robin weight=1 connect-fail-limit=2 allow-miss max-conn=5\n"
def update_conf(proxies):
    with open('/etc/squid/squid.conf.original', 'r') as F:
        squid_conf = F.readlines()
    squid_conf.append('\n# Cache peer config\n')
    for proxy in proxies:
        squid_conf.append(PEER_CONF % (proxy[0], proxy[1]))
    with open('/etc/squid/squid.conf', 'w') as F:
        F.writelines(squid_conf)
def get_proxy():
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
        # 2. 写入Squid配置文件
        update_conf(proxies)
        # 3. 重新加载配置文件
        os.system('squid -k reconfigure')
        print 'done'
def main():
    start = time.time()
    while True:
        # 每60秒获取一批新IP
        if time.time() - start >= 60:
            get_proxy()
        time.sleep(5)
        start = time.time()
if __name__ == '__main__':
    main()
