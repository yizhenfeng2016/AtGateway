#-*- coding:utf-8 -*-
__author__ = 'Administrator'

import json
import requests
import time
import threading
from share import user
from share import queue
from share import logfile
from key import AESKey,RSAKey

# POST_SECUREPORT_URL="http://112.74.28.12/secureport"
# POST_MSG_URL="http://112.74.28.12/postmsg"
# GET_URL="http://112.74.28.12/getmsg"

AES_KEY="0000000000000000" #需要共享的变量
LOCK_KEY=threading.Lock() #锁

TOKEN=""
LOCK_TOKEN=threading.RLock() #锁

class PubPost(RSAKey):
    def request_post(self,msg):
        msg=json.dumps(msg)
        miwen=self._pub_encrypt(msg)
        res_msg=""
        try:
            response=requests.post(url=user.get_info_dict("POST_SECUREPORT_URL"),data=miwen,timeout=1)
            if response.status_code==200:
                res_msg=self._pub_decrypt(response.content)
        except requests.ConnectionError as e: #断开连接了
            # print("PubPost connection error")
            # print("PubPost post===",e.message)
            # time.sleep(60)
            logfile.logger.exception(e.message)
        except Exception as e:
            # print("PubPost post===",e.message)
            logfile.logger.exception(e.message)
        finally:
            return res_msg

class SendMsg(AESKey):
    def _request(self,method,params=None,msg=None): #只有实例和子类使用
        global AES_KEY
        global LOCK_KEY
        global TOKEN
        global LOCK_TOKEN
        res_msg=""
        response=""
        try:
            if method=="get":
                # print("come in get server")
                if LOCK_TOKEN.acquire():
                    param={
                        "token":TOKEN
                    }
                    LOCK_TOKEN.release()
                    param.update(params)

                    try:
                        response=requests.get(url=user.get_info_dict("GET_URL"),params=param,timeout=65) #大多数请求外部服务器应该有一个超时,
                                                                                  # 以防服务器没有响应及时。没有超时,那么您的代码就会挂几分钟或者更多
                        temp_response="getReponseCode==="+str(response.status_code)
                        queue.logcat_Q.put(temp_response)

                    except requests.ConnectionError as e: #get服务断开连接，每60秒请求一次
                        # print(time.time())
                        # print("get connection error")
                        # print("SendMsg get===",e.message)
                        time.sleep(60)
                        # print("60s sleep over")
                    except requests.ConnectTimeout as e:
                        # print(time.time())
                        # print("get Timeout error")
                        # print("SendMsg get===",e.message)
                        pass
                    except Exception as e:
                        # print("SendMsg get===",e.message)
                        logfile.logger.exception(e.message)
            else :
                if LOCK_TOKEN.acquire():
                    sendmsg={
                        "token":TOKEN
                    }
                    LOCK_TOKEN.release()
                    sendmsg.update(msg)
                    # print(sendmsg)
                    jsonmsg=json.dumps(sendmsg)
                    # print(jsonmsg)
                    temp_msg="json.dumps()==="+jsonmsg
                    queue.logcat_Q.put(temp_msg)
                    if LOCK_KEY.acquire():
                        miwen=self._aes_encrypt(AES_KEY,jsonmsg)
                        LOCK_KEY.release()
                        try:
                            response=requests.post(url=user.get_info_dict("POST_MSG_URL"),data=miwen,timeout=2)
                            temp_response="postResponseCode==="+str(response.status_code)
                            queue.logcat_Q.put(temp_response)
                        except Exception as e:
                            # print("SendMsg post===",e.message)
                            logfile.logger.exception(e.message)
            if response!="":
                if response.status_code==200:
                    if LOCK_KEY.acquire():
                        try:
                            res_msg=self._aes_decrypt(AES_KEY,response.content)
                            queue.result_Q.put(res_msg)
                            temp_result="postResult==="+res_msg
                            queue.logcat_Q.put(temp_result)
                            LOCK_KEY.release()
                        except Exception as e:
                            # print("aes_decrypt",e.message)
                            temp_exception="aes_decrypt().Exception==="+e.message
                            queue.logcat_Q.put(temp_exception)
                            LOCK_KEY.release()#避免死锁
                            exptime=GetAesKey().get_aes()
                            # print("aes_decrypt fail:",exptime)
                            temp_exptime="AesKeyExpire==="+str(exptime)
                            queue.logcat_Q.put(temp_exptime)
        except Exception as e:
            # print(e.message)
             temp_exception="_request().Exception==="+e.message
             queue.logcat_Q.put(temp_exception)
        finally:
            return res_msg

class LoginManage(PubPost,SendMsg):
    def __init__(self):
        self.username=user.get_info_dict("USERNAME")
        self.password=user.get_info_dict("PASSWORD")

    def login(self):
        #登录，获取token--调通
        global TOKEN
        global LOCK_TOKEN
        try:
            msg={"cmd":"login","from_username":self.username,"password":self.password}
            # print(msg)
            res_msg=self.request_post(msg)
            if res_msg!="":
                res_msg2=dict(res_msg)
                # print(res_msg2)
                if res_msg2.get("result",None)=="success":
                    # print("Login success")
                    if LOCK_TOKEN.acquire():
                        TOKEN=res_msg2.get("token")
                        LOCK_TOKEN.release()
                    return "Login success"
                else:
                    return "Login failure"
            else:
                # print("check in the network and login again")
                return "check in the network and login again"
        except Exception as e:
            logfile.logger.exception(e.message)

    def loginout(self):
        #退出登录
        sendmsg={"cmd":"logout"}
        res_msg=self._request("post",msg=sendmsg)
        return res_msg

class GetAesKey(PubPost):
    def get_aes(self):
        #获取动态aes密码--调通
        global AES_KEY
        global LOCK_KEY
        expiretime=0
        try:
            timenow=str(int(time.time()))
            msg={"cmd":"get_dynamic_passwd","time":timenow}
            res_msg=self.request_post(msg)
            if res_msg!="":
                res_msg2=dict(res_msg)
                if LOCK_KEY.acquire():
                    AES_KEY=res_msg2.get("dynamic_passwd","0000000000000000")
                    # print("AESKEY change:",AES_KEY)
                    temp_key="AesKeyChange==="+AES_KEY
                    queue.logcat_Q.put(temp_key)
                    LOCK_KEY.release()
                    expiretime=int(res_msg2.get("expire",0))
        except Exception as e:
            logfile.logger.exception(e.message)
        finally:
            return int(expiretime/1000)
