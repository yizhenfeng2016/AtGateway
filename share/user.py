#-*- coding:utf-8 -*-
__author__ = 'Administrator'

import threading
import socket
import time

# USERNAME=""
# PASSWORD=""
# SIPADDR=""
# PID=""
# VID="0000"

#pid:设备号，舒睡宝是“0001”室内机0002,协调器“0003”
#空气盒子0004, WIFI门锁0005,服务型机器人0006，扫地机0007,魔镜：0008，无屏主机0009

# Net_flag=0
# SERVER_IP=""
# SERVER_PORT=9102
# data_length=6
# Protocol_flag="smartProtocol"
#
# getHttp="http://{0}/lua/getall".format(SERVER_IP)
# postHttp="http://{0}/lua".format(SERVER_IP)

info_dict={
    "VID":"0000"
}
info_lock=threading.RLock()
def get_info_dict(key):
    global info_dict
    global info_lock
    info=""
    if info_lock.acquire():
        info=info_dict.get(key,None)
        info_lock.release()
    return info

def set_info_dict(key,value):
    global info_dict
    global info_lock
    if info_lock.acquire():
        info_dict[key]=value
        info_lock.release()

data_dict={}#key:"usr","rooms","devices","combs","search"要加锁
data_lock=threading.RLock()
def get_data_dict(key):
    global data_dict
    global data_lock
    data=""
    if data_lock.acquire():
        data=data_dict.get(key,None)
        data_lock.release()
    return data

def set_data_dict(key,value):
    global data_dict
    global data_lock
    if data_lock.acquire():
        data_dict[key]=value
        data_lock.release()

# timeout =90
# socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
TCP_SOCKET=socket.socket()
# SOCKET_LOCK=threading.RLock()
def create_tcp_socket(ip,port):
    global TCP_SOCKET
    # global SOCKET_LOCK
    TCP_SOCKET=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    TCP_SOCKET.settimeout(1)
    connect_flag=0
    try:
        TCP_SOCKET.connect((ip,port))
        # print(TCP_SOCKET)
        connect_flag=1
    except Exception as e:
        # print("create tcp socket failure")
        connect_flag=0
    finally:
        return connect_flag
