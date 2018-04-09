#-*- coding:utf-8 -*-
__author__ = 'Administrator'

import json
import threading
import time
import requests
from share import user
from share import queue
from share import logfile
from key import AESKey

import re

private_key="2dc12e1181bec212"
dynamic_key=""
key_lock=threading.RLock()

login_flag=True
login_lock=threading.RLock()

APP_ID="1000000002"

getHttpToken=""

class SendRecvManage(AESKey):
    def login(self):
        global login_flag
        global login_lock
        login_success_flag=0
        dict_msg={
            "msg_type": "gateway_manager",
            "from_role": "shared_company",
            "command": "login",
            "from_account": user.get_info_dict("USERNAME"),
            "app_id": APP_ID
        }
        if user.get_info_dict("SERVER_PORT")==9102:
             dict_msg={
                "msg_type": "gateway_manager",
                "from_role": "shared_company",
                "command": "login",
                "from_account": user.get_info_dict("USERNAME"),
                "app_id": APP_ID,
                "password": ""
            }
        self.send_all(dict_msg,flag="private")
        time.sleep(2)
        if key_lock.acquire():
            if dynamic_key and login_flag:
                # print("login success")
                login_success_flag=1
            key_lock.release()

        if login_lock.acquire():
            login_flag=True
            login_lock.release()
        return login_success_flag

    def send_all(self,dict_msg,flag="dynamic"):
        global dynamic_key
        global key_lock
        # python json不编码unicode并且除去无用的空格
        # data = json.dumps(data,separators=(‘,’,’:’),ensure_ascii=False)
        msg=json.dumps(dict_msg,separators=(',',':'))
        # print(msg)
        queue_msg="send success==="+msg
        queue.logcat_Q.put(queue_msg)
        temp_msg={}
        if flag=="private":
            encrypt_msg=self._aes_encrypt(private_key,msg)
            temp_msg={
                "encrypt":"private",
                "msg":encrypt_msg,
                "app_id":APP_ID
            }
        else:
            if key_lock.acquire():
                # print(dynamic_key)
                encrypt_msg=self._aes_encrypt(dynamic_key,msg)
                key_lock.release()
                if user.get_info_dict("SERVER_PORT")==9101:
                    temp_msg={
                        "msg":encrypt_msg,
                        "encrypt":"dynamic",
                        "app_id":APP_ID
                    }
                elif user.get_info_dict("SERVER_PORT")==9102:
                    if getHttpToken:
                        temp_msg={
                            "msg":encrypt_msg,
                            "encrypt":"dynamic",
                            "app_id":APP_ID,
                            "token":getHttpToken
                        }
        str_temp_msg=json.dumps(temp_msg,separators=(',',':'))
        if user.get_info_dict("SERVER_PORT")==9101: #室内机或魔镜内网
            str_len=self.__fourhex(str_temp_msg)
            if user.get_info_dict("data_length")==6:
                str_len=self.__sixhex(str_temp_msg)
            temp="smartProtocol"+str_len
            send_msg=temp+str_temp_msg
            queue_msg="send to business==="+send_msg
            queue.logcat_Q.put(queue_msg)
            # print(user.TCP_SOCKET)
            try:
                # print("tcp send")
                user.TCP_SOCKET.settimeout(1)#设置超时1s
                user.TCP_SOCKET.sendall(send_msg)
            except Exception as e: #超时
                # print("send to server,is not connect")
                # print(e.message)
                logfile.logger.exception(e.message)

        elif user.get_info_dict("SERVER_PORT")==9102:  #zigbee内网
            try:
                res=requests.post(url=user.get_info_dict("postHttp"),data=str_temp_msg,timeout=1)
                # print(res.status_code)
                # print("post from zigbee result===",res.content)
                queue_msg="post from zigbee getReponseCode==="+str(res.status_code)
                # print(queue_msg)
                queue.logcat_Q.put(queue_msg)
                if res.status_code==200:
                    self.__msg_decrypt(res.content)
            except requests.ConnectionError as e: #断开连接了
                # print("zigbee connection error")
                # print("zigbee post===",e.message)
                pass
            except Exception as e:
                # print(e.message)
                logfile.logger.exception(e.message)

    def recv_all(self):
        #data length is packed into 4 or 6 bytes
        if user.get_info_dict("SERVER_PORT")==9101:
            size_data=''
            sock_data=''
            recv_size=8192
            try:
                # print(user.TCP_SOCKET)
                user.TCP_SOCKET.settimeout(90) #设置超时90s
                sock_data=user.TCP_SOCKET.recv(recv_size)
                data_size_flag=17
                if user.get_info_dict("data_length")==6:
                    data_size_flag=19
                if len(sock_data)>data_size_flag:
                    size_data=size_data+sock_data
                    # print(size_data)
                    # print(size_data[13:data_size_flag])
                    size=int(size_data[13:data_size_flag],16)
                    # print(size)
                    if size>len(size_data):
                        while True:
                            sock_data=user.TCP_SOCKET.recv(recv_size)
                            size_data=size_data+sock_data
                            if size<=len(size_data):
                                break

                if size_data!="":
                    queue_msg="from business==="+size_data
                    queue.logcat_Q.put(queue_msg)
                    self.__do_msg(size_data,data_size_flag)

            except Exception as e:
                # print("is not connect ")
                # print(e.message)
                # logfile.logger.exception(e.message)
                # user.TCP_SOCKET.close()
                # print("waiting 3s")
                time.sleep(3)
                while True:
                    # print("reconnect again")
                    # print("ip:",(user.get_info_dict("SERVER_IP"),user.get_info_dict("SERVER_PORT")))
                    connect_flag=user.create_tcp_socket(user.get_info_dict("SERVER_IP"),user.get_info_dict("SERVER_PORT"))#重新连接
                    if connect_flag:
                        # print("reconnect success")
                        # print("login again")
                        self.login()
                        break
                    else:
                        # print("reconnect failure")
                        # print("waiting 60s")
                        time.sleep(60)
                # print("re connect tcp server success")

        elif user.get_info_dict("SERVER_PORT")==9102:
            if getHttpToken:
                params={
                    "tok":getHttpToken,
                    "id":APP_ID
                }
                try:
                    res=requests.get(url=user.get_info_dict("getHttp"),params=params,timeout=30)
                    queue_msg="get from zigbee getReponseCode==="+str(res.status_code)
                    queue.logcat_Q.put(queue_msg)
                    # print(queue_msg)
                    if res.status_code==200:
                        # print("come in msg_decrypt")
                        self.__msg_decrypt(res.content)
                except requests.ConnectionError as e: #断开连接，每1分钟请求一次
                    # print("zigbee connection error")
                    # print("zigbee get===",e.message)
                    # print("waiting 60s")
                    time.sleep(60)
                except requests.ConnectTimeout as e:
                    # print(time.time())
                    # print("get Timeout error")
                    # print("RecvMsg get===",e.message)
                    # logfile.logger.exception(e.message)
                    pass
                except Exception as e:
                    # print("RecvMsg get===",e.message)
                    logfile.logger.exception(e.message)

    def __do_msg(self,recv_msg,data_size_flag): #处理完整data
        total_len=len(recv_msg)
        str_start=0
        str_stop=0
        try:
            if total_len>data_size_flag:
                while str_stop<total_len:
                    msg_len=int(recv_msg[str_stop+13:str_stop+data_size_flag],16)
                    str_start=str_stop+data_size_flag
                    str_stop=str_stop+msg_len+data_size_flag
                    if total_len>=str_stop:
                        # print(msg_len)
                        msg_data=recv_msg[str_start:str_stop]
                        # print(msg_data)
                        self.__msg_decrypt(msg_data)
        except Exception as e:
            logfile.logger.exception(e.message)

    def __msg_decrypt(self,msg_data):#解密
        global dynamic_key
        global login_flag
        global key_lock
        global login_lock
        global getHttpToken
        try:
            dict_msg=dict(eval(msg_data))
            encrypt=dict_msg.get("encrypt",None)
            # print("encrypt way===",encrypt)
            msg=dict_msg.get("msg",None)
            # print("msg===",msg)
            if encrypt=="private":
                jiemi_msg=self._aes_decrypt(private_key,msg)
                # if jiemi_msg[0]=='[' and jiemi_msg[-1]==']':
                #     jiemi_msg=jiemi_msg[1:-1]
                jiemi_msg=re.findall(r"{(.*)}",jiemi_msg)
                for l in jiemi_msg:
                    jiemi_json='{'+l+'}'
                    queue.result_Q.put(jiemi_json)
                    queue_msg="get result==="+jiemi_json
                    queue.logcat_Q.put(queue_msg)
                # jiemi_msg=jiemi_msg.replace('[','').replace(']','')
                    try:
                        dict_jiemi_msg=dict(eval(jiemi_json))
                        # print("dict===",dict_jiemi_msg)
                        if dict_jiemi_msg.get("dynamic_key",None):
                            # print("get dynamic key")
                            if key_lock.acquire():
                                dynamic_key=dict_jiemi_msg.get("dynamic_key")
                                # print("dynamic_key===",dynamic_key)
                                key_lock.release()
                        if dict_jiemi_msg.get("token",None):
                            getHttpToken=dict_jiemi_msg.get("token")
                        if dict_jiemi_msg.get("command",None)=="loginout":
                            if login_lock.acquire():
                                login_flag=False
                                login_lock.release()

                    except Exception as e:
                        # print(e.message)
                        logfile.logger.exception(e.message)
            else:
                if key_lock.acquire():
                    key=dynamic_key
                    key_lock.release()
                    jiemi_msg=self._aes_decrypt(key,msg)
                    # if jiemi_msg[0]=='[' and jiemi_msg[-1]==']':
                    #     jiemi_msg=jiemi_msg[1:-1]
                    jiemi_msg=re.findall(r"{(.*)}",jiemi_msg)
                    for l in jiemi_msg:
                        jiemi_json='{'+l+'}'
                        queue.result_Q.put(jiemi_json)
                        queue_msg="get result==="+jiemi_json
                        queue.logcat_Q.put(queue_msg)
                        # print(queue_msg)
        except Exception as e:
            logfile.logger.exception(e.message)

    def __fourhex(self,msg):
        str_len_hex=hex(len(msg))
        len_hex=str_len_hex[2:]
        len_hex_result=""
        if len(len_hex)==1:
            len_hex_result="000"+len_hex
        elif len(len_hex)==2:
            len_hex_result="00"+len_hex
        elif len(len_hex)==3:
            len_hex_result="0"+len_hex
        else:
            len_hex_result=len_hex
        return len_hex_result

    def __sixhex(self,msg):
        str_len_hex=hex(len(msg))
        len_hex=str_len_hex[2:]
        len_hex_result=""
        if len(len_hex)==1:
            len_hex_result="00000"+len_hex
        elif len(len_hex)==2:
            len_hex_result="0000"+len_hex
        elif len(len_hex)==3:
            len_hex_result="000"+len_hex
        elif len(len_hex)==4:
            len_hex_result="00"+len_hex
        elif len(len_hex)==5:
            len_hex_result="0"+len_hex
        else:
            len_hex_result=len_hex
        return len_hex_result