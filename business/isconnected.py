#coding:utf-8
__author__ = 'Administrator'

import requests
connectHttp="http://112.74.28.12"

def can_remote_connect():
    try:
        res=requests.get(url=connectHttp,timeout=0.1)
        if res.status_code==200:
            # connect_flag=1
            return 1  #连接成功
        else:
            return 0 #连接失败
    except requests.ConnectionError:
        print("ConnectionError")
        return 0
    except requests.ConnectTimeout:
        print("ConnectTimeout")
        return 2 #连接超时
    except requests.HTTPError:
        print("HTTPError")
        return 3 #无效HTTP响应