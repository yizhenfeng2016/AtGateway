#coding:utf-8
__author__ = 'Administrator'

import socket
from key import AESKey
import json
from share import user

SEARCH_KEY="atsmart201511049"

class SearchDevice(AESKey):
    def search(self,PORT=9200,BufferSize=8192):
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(1)
        HOST='<broadcast>'
        #PORT 9200：网关与其他设备；9100：室内机和魔镜
        if user.get_info_dict("PID")=="0002" or user.get_info_dict("PID")=="0008":
            PORT=9100
        elif user.get_info_dict("PID")=="0003":
            PORT=9200
        # print(PORT)
        ADDR=(HOST,PORT) #向9200端口的设备发送广播消息
        sock.bind(('',0))
        msg={
            "msg_type": "search",
            "from_role": "phone",
            "from_account": user.get_info_dict("USERNAME"),
            "command": "query",
            "app_id": "1000000002"
        }
        msg=json.dumps(msg,separators=(',',':'))
        jiami_msg=self._aes_encrypt(SEARCH_KEY,msg)
        # print(jiami_msg)
        sock.sendto(jiami_msg,ADDR)
        devices_list=[]
        while True:
            try:
                data,addr=sock.recvfrom(BufferSize)
                rec_data=self._aes_decrypt(SEARCH_KEY,data)
                # print("got data from",addr)
                # print(rec_data)
                rec_data=dict(eval(rec_data))
                devices_list.append(rec_data)
            except Exception as e:
                # print(e.message)
                break
        sock.close()
        user.set_data_dict("search",devices_list)