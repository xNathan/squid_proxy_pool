# squid 代理池搭建

## 简介

使用squid以及收费代理搭建爬虫代理池，自动获取最新可用代理并写入squid配置文件。

具体介绍及思路参考文章：[自己搭建亿级爬虫IP代理池](http://www.xnathan.com/2017/03/02/squid-proxy-pool/)

## 运行

1. 备份原始squid配置文件
   `sudo cp /etc/squid/squid.conf /etc/squid/squid.conf`

2. 购买 [站大爷](http://ip.zdaya.com) 短效代理 API，修改 `zdy.py`，将 `api_url = 'http://s.zdaye.com/?api=YOUR_API&count=100&fitter=1&px=2'` 改为自己的 api 地址

3. 运行 `sudo python zdy.py`，由于要写文件和重新加载配置，所以要使用 `sudo` 运行。

## 检测

修改 `test_proxy.py` 中 `139.xxx.xxx.66:3188` 为自己的 squid 服务器地址，每次运行 `test_proxy.py` 都会有不同的ip，表明代理搭建成功。

## TODO

- [ ] 重构代码，避免使用全局变量
- [ ] 支持多种类型的代理 API 接口，不只限定于站大爷