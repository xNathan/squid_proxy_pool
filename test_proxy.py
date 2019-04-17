#!/usr/bin/env python
# coding: utf-8
"""
代理IP池实例演示
"""
from __future__ import print_function

import requests

s = requests.Session()
s.proxies.update({"http": "139.xxx.xxx.66:3188"})
print(s.get("http://httpbin.org/ip"))
