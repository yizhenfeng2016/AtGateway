#-*- coding:utf-8 -*-
__author__ = 'Administrator'

from business.remote import SendMsg
from business.local import SendRecvManage
import json
from share import user

class QueryMsg(SendMsg,SendRecvManage):
    def security_mode_query(self):
        self.__send_msg("security_mode_change")

    def room_query(self):
        params={
            "room_id":-1
        }
        self.__send_msg("room_manager",extend_params=params)

    def devices_query(self):
        params={
            "query_all":"yes",
        }
        self.__send_msg("device_manager",extend_params=params)

    def combination_control_query(self):
        params={
            "comb_control_id":-1
        }
        self.__send_msg("combination_control_manager",extend_params=params)

    def more_control_query(self):
        params={
            "m_c_name":"more_control_device"
        }
        self.__send_msg("combination_control_manager",extend_params=params)

    def module_state_info_query(self):
        self.__send_msg("module_state_info")

    def alarm_log_query(self,offset=0,count=15):
        params={
            "offset":offset,
            "count":count
        }
        self.__send_msg("alarm_logs_info",extend_params=params)

    def alarm_pics_query(self,log_id=1):
        params={
            "log_id":log_id
        }
        self.__send_msg("alarm_pics_info",extend_params=params)

    def __send_msg(self,msg_type,extend_params=None):
        if user.get_info_dict("Net_flag")==1:
            cmd={
                "msg_type":msg_type,
                "command":"query",
                "from_role":"phone",
                "from_account":user.get_info_dict("USERNAME")
            }
            if extend_params:
                cmd.update(extend_params)
            sendmsg=self.__sendmsgformat(cmd)
            # print(sendmsg)
            res_msg=self._request("post",msg=sendmsg)
            # print(res_msg)

        elif user.get_info_dict("Net_flag")==0:
            cmd={
                "msg_type":msg_type,
                "command":"query",
                "from_role":"phone",  #用"phone"or"shared_company"?  OK
                "from_account":user.get_info_dict("USERNAME")
            }
            if extend_params:
                cmd.update(extend_params)
            self.send_all(cmd,flag="dynamic")


    def __sendmsgformat(self,msg=None):
        sendmsg={
            "cmd":"send_msg",
            "to_username":user.get_info_dict("SIPADDR"),
            "msg":json.dumps(msg),
            "subject":"control"
             }
        return sendmsg

    def get_dev_status(self):
        sendmsg={
            "cmd":"get_dev_status",
            "offset":"0",
            "total":"1048576",#1024*1024=1048576
            "pid":user.get_info_dict("PID"),
            "vid":user.get_info_dict("VID"),
            "to_username":user.get_info_dict("SIPADDR")
        }
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        if res_msg!="":
            self.OnDataCallback(res_msg)
        # print(res_msg)

    def get_all_friends(self):
        sendmsg={"cmd":"get_allfriend","offset":"0","total":"100"}
        # print(sendmsg)
        res_msg=self._request("post",msg=sendmsg)
        if res_msg!="":
            self.OnDataCallback(res_msg)
        # print(res_msg)

    def OnDataCallback(self,msg):
        resmsg_dict=dict(eval(msg))
        if resmsg_dict.get("result",None)=="success":
            if resmsg_dict.get("usr",None):
                resmsg_usr_list=resmsg_dict.get("usr")
                user.set_data_dict("usr",resmsg_usr_list)
                # user.data_dict["usr"]=resmsg_usr_list
                # for l in resmsg_usr_list:
                #     print(json.dumps(l,encoding="UTF-8",ensure_ascii=False))
            elif resmsg_dict.get("devlist",None):
                dev_list=resmsg_dict.get("devlist")
                rooms_list=dev_list[0]["rooms"]
                user.set_data_dict("rooms",rooms_list)
                # user.data_dict["rooms"]=rooms_list
                devices_list=dev_list[0]["devices"]
                user.set_data_dict("devices",devices_list)
                # user.data_dict["devices"]=devices_list
                combs_list=dev_list[0]["combs"]
                user.set_data_dict("combs",combs_list)
                # user.data_dict["combs"]=combs_list
                # for l in rooms_list:
                #     print(json.dumps(l,encoding="UTF-8",ensure_ascii=False))
                # for l in devices_list:
                #     print(json.dumps(l,encoding="UTF-8",ensure_ascii=False))
                # for l in combs_list:
                #     print(json.dumps(l,encoding="UTF-8",ensure_ascii=False))

