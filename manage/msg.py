#-*- coding:utf-8 -*-
__author__ = 'Administrator'

from business.remote import SendMsg,LoginManage
from business.local import SendRecvManage
import time
import threading
import json
from share import queue
from share import user
from share import logfile

class GetMsg(SendMsg):
    def get_msg(self):
        param={
            "role":"phone"
        }
        result_msg=self._request("get",params=param)
        if result_msg!="":
            temp_result="getResult==="+result_msg
            queue.logcat_Q.put(temp_result)
            # print(time.time())
            # print(result_msg)
        # else:
        #   # print(time.time())
            # print("result_msg is """)

def OnDataCallback():
    getresult=""
    if not queue.logcat_Q.empty():
        getresult=queue.logcat_Q.get()
    return getresult

class ResultOnCallBack(SendMsg,SendRecvManage):
    def res_heartbeat(self,msg):
        cmd={
            "result":"success"
        }
        msg.update(cmd)
        self.send_all(msg,flag="dynamic")

    def res_login(self):
        self.login()

    def result_deal(self):
        """
        处理队列返回类似{}类型的数据，因为必须要转化成python的dict对象，若不是，请在放数据进队列之前
        转化成只有带{}的内容
        """
        if not queue.result_Q.empty():
            # print("come in result_deal")
            resmsg=queue.result_Q.get()
            if resmsg:
                try:
                    msg=dict(eval(resmsg))
                    if msg.get("msg",None):
                        temp_msg=msg.get("msg")
                        msg=dict(eval(temp_msg))
                    if msg.get("result",None)=="success":
                        if msg.get("msg_type",None)=="combination_control_manager":
                            combs_list=msg.get("combs")
                            if combs_list:
                                user.set_data_dict("combs",combs_list)
                                # user.data_dict["combs"]=combs_list
                                # for l in combs_list:
                                #     print(json.dumps(l,encoding="UTF-8",ensure_ascii=False))
                        elif msg.get("msg_type",None)=="room_manager":
                            rooms_list=msg.get("rooms")
                            if rooms_list:
                                user.set_data_dict("rooms",rooms_list)
                                # user.data_dict["rooms"]=rooms_list
                                # for l in rooms_list:
                                #     print(json.dumps(l,encoding="UTF-8",ensure_ascii=False))
                        elif  msg.get("msg_type",None)=="device_manager":
                            devices_list=msg.get("devices")
                            if devices_list:
                                user.set_data_dict("devices",devices_list)
                                # user.data_dict["devices"]=devices_list
                                # for l in devices_list:
                                #     print(json.dumps(l,encoding="UTF-8",ensure_ascii=False))

                    elif msg.get("msg_type",None)=="heartbeat" and msg.get("from_role",None)=="business":#室内机内网
                        # print(time.time())
                        # print(msg)
                        self.res_heartbeat(msg)

                    elif msg.get("result",None)=="forced_exit" and msg.get("command",None)=="loginout":
                        # print("local network gateway or mirror")
                        queue.logout_Q.put("forced_exit")

                    elif msg.get("from_role",None)=="coordin_zigbee" and msg.get("msg_type",None)=="heartbeat" and msg.get("reason",None)=="token_error": #zigbee内网
                        # print("token error,login again")
                        # print(time.time())
                        # print(msg)
                        self.res_login()

                    elif msg.get("from_role",None)=="coordin_zigbee" and msg.get("msg_type",None)=="someone_login":
                        # print(time.time())
                        # print("someone_login,login again")
                        queue.logout_Q.put("someone_login_zigbee")

                    elif msg.get("result",None)=="token_error" and msg.get("cmd",None)!="logout": #公网
                        # print("token error,login again")
                        flag=LoginManage().login()
                        # print(flag)

                    elif msg.get("result",None)=="someone_login":
                        # print("someone_login,login again")
                        queue.logout_Q.put("someone_login")

                except Exception as e:
                    # print(e.message)
                    logfile.logger.exception(e.message)