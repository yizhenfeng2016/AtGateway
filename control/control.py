#-*- coding:utf-8 -*-
__author__ = 'Administrator'

from business.remote import SendMsg
from business.local import SendRecvManage
from share import user
import time
import json
import hashlib

class Control(SendMsg,SendRecvManage):
    def __init__(self):
        self.default_time=0.2

    def devices_c(self,dev_class_type,cmd_list):
        if dev_class_type=="light": #开关
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.light_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==4: #第4为表示延时
                time.sleep(int(cmd_list[3]))
                self.light_c(cmd_list[0],cmd_list[1],cmd_list[2])

        elif dev_class_type=="curtain": #窗帘
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.curtain_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==4:#第4为表示延时
                time.sleep(int(cmd_list[3]))
                self.curtain_c(cmd_list[0],cmd_list[1],cmd_list[2])


        elif dev_class_type=="fresh_air_system": #新风系统
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.fresh_air_system_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==4:#第4为表示延时
                time.sleep(int(cmd_list[3]))
                self.fresh_air_system_c(cmd_list[0],cmd_list[1],cmd_list[2])


        elif dev_class_type=="dimmer": #可调光
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.dimmer_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==4: #第4位判断是否延时还是调光
                if cmd_list[2]=="brightness":
                    value=int(cmd_list[3])
                    time.sleep(self.default_time)
                    self.dimmer_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)

                else: #延时
                    value=int(cmd_list[3])
                    time.sleep(value)
                    self.dimmer_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==5: #调光延时
                value=int(cmd_list[3])
                time.sleep(int(cmd_list[4]))
                self.dimmer_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)


        elif dev_class_type=="smartlock": #锁
            if len(cmd_list)==4:
                time.sleep(self.default_time)
                self.smartlock_c(cmd_list[0],cmd_list[1],cmd_list[2],cmd_list[3])

            elif len(cmd_list)==5: #延时
                time.sleep(int(cmd_list[4]))
                self.smartlock_c(cmd_list[0],cmd_list[1],cmd_list[2],cmd_list[3])


        elif dev_class_type=="smartlock_hl": #锁
            if len(cmd_list)==4:
                time.sleep(self.default_time)
                self.smartlock_hl_c(cmd_list[0],cmd_list[1],cmd_list[2],cmd_list[3])

            elif len(cmd_list)==5: #延时
                time.sleep(int(cmd_list[4]))
                self.smartlock_hl_c(cmd_list[0],cmd_list[1],cmd_list[2],cmd_list[3])


        elif dev_class_type=="smartlock_at": #锁
            if len(cmd_list)==4:
                time.sleep(self.default_time)
                self.smartlock_at_c(cmd_list[0],cmd_list[1],cmd_list[2],cmd_list[3])

            elif len(cmd_list)==5: #延时
                time.sleep(int(cmd_list[4]))
                self.smartlock_at_c(cmd_list[0],cmd_list[1],cmd_list[2],cmd_list[3])


        elif dev_class_type=="aircondition": #空调
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.air_condition_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==4:
                if cmd_list[2]=="temperature":
                    value=int(cmd_list[3])
                    time.sleep(self.default_time)
                    self.air_condition_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)

                else:
                    value=int(cmd_list[3])
                    time.sleep(value)
                    self.air_condition_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==5: #温度调节延时
                value=int(cmd_list[3])
                time.sleep(int(cmd_list[4]))
                self.air_condition_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)


        elif dev_class_type=="icool": #icool
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.icool_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==4:
                if cmd_list[2]=="temperature":
                    value=int(cmd_list[3])
                    time.sleep(self.default_time)
                    self.icool_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)

                else:
                    value=int(cmd_list[3])
                    time.sleep(value)
                    self.icool_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==5: #温度调节延时
                value=int(cmd_list[3])
                time.sleep(int(cmd_list[4]))
                self.icool_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)


        elif dev_class_type=="tv": #电视
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.tv_c(cmd_list[0],cmd_list[1],cmd_list[2])
            elif len(cmd_list)==4:
                if cmd_list[2]=="channel":
                    value=int(cmd_list[3])
                    time.sleep(self.default_time)
                    self.self.tv_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)

                else:
                    value=int(cmd_list[3])
                    time.sleep(value)
                    self.self.tv_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==5:
                value=int(cmd_list[3])
                time.sleep(int(cmd_list[4]))
                self.tv_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)


        elif dev_class_type=="dvb": #机顶盒
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.dvb_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==4:
                if cmd_list[2]=="channel":
                    value=int(cmd_list[3])
                    time.sleep(self.default_time)
                    self.dvb_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)

                else:
                    value=int(cmd_list[3])
                    time.sleep(value)
                    self.dvb_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==5:
                value=int(cmd_list[3])
                time.sleep(int(cmd_list[4]))
                self.dvb_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)


        elif dev_class_type=="dvd": #dvd
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.dvd_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==4: #第4为表示延时
                time.sleep(int(cmd_list[3]))
                self.dvd_c(cmd_list[0],cmd_list[1],cmd_list[2])


        elif dev_class_type=="amplifier": #功放
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.amplifier_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==4: #第4为表示延时
                time.sleep(int(cmd_list[3]))
                self.amplifier_c(cmd_list[0],cmd_list[1],cmd_list[2])


        elif dev_class_type=="dryingracks": #晾衣架
        #     3:"dis_on",
        #     4:"dis_off",
        #     5:"bakedry_on",
        #     6:"bakedry_off",
        #     7:"winddry_on",
        #     8:"winddry_off",
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.dryingracks_c(cmd_list[0],cmd_list[1],cmd_list[2])
            elif len(cmd_list)==4:
                if cmd_list[2]=="dis_on" or cmd_list[2]=="bakedry_on" or cmd_list[2]=="winddry_on":
                    value=int(cmd_list[3])
                    time.sleep(self.default_time)
                    self.dryingracks_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)

                else:
                    value=int(cmd_list[3])
                    time.sleep(value)
                    self.dryingracks_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==5:
                value=int(cmd_list[3])
                time.sleep(int(cmd_list[4]))
                self.dryingracks_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)


        elif dev_class_type=="rgb_light": #灯带
        #     2:"brightness",
        #     3:"rgb_toning",
        #     4:"rgb_mode",
        #     5:"rgb_toning_brightness"
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.rgb_light_c([0],cmd_list[1],cmd_list[2])


            elif len(cmd_list)==4:  #调光
                if cmd_list[2]=="brightness":
                    value=int(cmd_list[3])
                    time.sleep(self.default_time)
                    self.rgb_light_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)

                else: #延时
                    value=int(cmd_list[3])
                    time.sleep(value)
                    self.rgb_light_c(cmd_list[0],cmd_list[1],cmd_list[2])
                    time.sleep(value)

            elif len(cmd_list)==5:  #渐变  调光延时
                if cmd_list[2]=="rgb_mode":
                    rgb_mode=cmd_list[3]
                    speed=int(cmd_list[4])
                    time.sleep(self.default_time)
                    self.rgb_light_c(cmd_list[0],cmd_list[1],cmd_list[2],rgb_mode=rgb_mode,speed=speed)

                else:
                    value=int(cmd_list[3])
                    time.sleep(int(cmd_list[4]))
                    self.rgb_light_c(cmd_list[0],cmd_list[1],cmd_list[2],value=value)


            elif len(cmd_list)==6: #取色 渐变延时
                if cmd_list[2]=="rgb_toning":
                    r=int(cmd_list[3])
                    g=int(cmd_list[4])
                    b=int(cmd_list[5])
                    time.sleep(self.default_time)
                    self.rgb_light_c(cmd_list[0],cmd_list[1],cmd_list[2],r=r,g=g,b=b)

                else: #渐变延时
                    rgb_mode=cmd_list[3]
                    speed=int(cmd_list[4])
                    value=int(cmd_list[5])
                    time.sleep(value)
                    self.rgb_light_c(cmd_list[0],cmd_list[1],cmd_list[2],rgb_mode=rgb_mode,speed=speed)


            elif len(cmd_list)==7: #取色与调光 取色延时
                if cmd_list[2]=="rgb_toning_brightness":
                    brightness=int(cmd_list[3])
                    r=int(cmd_list[4])
                    g=int(cmd_list[5])
                    b=int(cmd_list[6])
                    time.sleep(self.default_time)
                    self.rgb_light_c(cmd_list[0],cmd_list[1],cmd_list[2],brightness=brightness,r=r,g=g,b=b)

                else: #取色延时
                    r=int(cmd_list[3])
                    g=int(cmd_list[4])
                    b=int(cmd_list[5])
                    value=int(cmd_list[6])
                    time.sleep(value)
                    self.rgb_light_c(cmd_list[0],cmd_list[1],cmd_list[2],r=r,g=g,b=b)


            elif len(cmd_list)==8: #取色与调光延时
                brightness=int(cmd_list[3])
                r=int(cmd_list[4])
                g=int(cmd_list[5])
                b=int(cmd_list[6])
                time.sleep(int(cmd_list[7]))
                self.rgb_light_c(cmd_list[0],cmd_list[1],cmd_list[2],brightness=brightness,r=r,g=g,b=b)


        elif dev_class_type=="coordin_xz_speaker": #小智
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.coordin_xz_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2])

            elif len(cmd_list)==4:
                time.sleep(int(cmd_list[3]))
                self.coordin_xz_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2])


        elif dev_class_type=="coordin_at_speaker": #4.5
        #     8:"volume",
        #     9:"play_mode",
        #     10:"audio_src"
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2])


            elif len(cmd_list)==4:
                if cmd_list[2]=="volume": #调节音量
                    volume=int(cmd_list[3])
                    time.sleep(self.default_time)
                    self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2],volume=volume)

                elif cmd_list[2]=="play_mode": #播放模式
                    play_mode=cmd_list[3]
                    time.sleep(self.default_time)
                    self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2],play_mode=play_mode)

                else: #其它延时
                    time.sleep(int(cmd_list[3]))
                    self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2])


            elif len(cmd_list)==5: #调节音量和播放模式延时
                if cmd_list[2]=="volume": #调节音量
                    volume=int(cmd_list[3])
                    time.sleep(int(cmd_list[4]))
                    self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2],volume=volume)

                elif cmd_list[2]=="play_mode": #播放模式
                    play_mode=cmd_list[3]
                    time.sleep(int(cmd_list[4]))
                    self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2],play_mode=play_mode)


        elif dev_class_type=="speaker_panel": #贝斯普
        #     8:"volume",
        #     9:"play_mode",
        #     10:"audio_src"
            if len(cmd_list)==3:
                time.sleep(self.default_time)
                self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2])


            elif len(cmd_list)==4:
                if cmd_list[2]=="volume": #调节音量
                    volume=int(cmd_list[3])
                    time.sleep(self.default_time)
                    self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2],volume=volume)

                elif cmd_list[2]=="play_mode": #播放模式
                    play_mode=cmd_list[3]
                    time.sleep(self.default_time)
                    self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2],play_mode=play_mode)

                elif cmd_list[2]=="audio_src": #音源模式
                    audio_src=cmd_list[3]
                    time.sleep(self.default_time)
                    self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2],audio_src=audio_src)

                else: #其它延时
                    time.sleep(int(cmd_list[3]))
                    self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2])


            elif len(cmd_list)==5: #调节音量/播放模式/音源模式延时
                if cmd_list[2]=="volume": #调节音量
                    volume=int(cmd_list[3])
                    time.sleep(int(cmd_list[4]))
                    self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2],volume=volume)

                elif cmd_list[2]=="play_mode": #播放模式
                    play_mode=cmd_list[3]
                    time.sleep(int(cmd_list[4]))
                    self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2],play_mode=play_mode)

                elif cmd_list[2]=="audio_src": #音源模式
                    audio_src=cmd_list[3]
                    time.sleep(int(cmd_list[4]))
                    self.coordin_at_speaker_c(cmd_list[0],cmd_list[1],cmd_list[2],audio_src=audio_src)


        elif dev_class_type=="combs": #场景
            if len(cmd_list)==1:
                time.sleep(self.default_time)
                self.scene_c(cmd_list[0])

            elif len(cmd_list)==2:
                time.sleep(int(cmd_list[1]))
                self.scene_c(cmd_list[0])



    def light_c(self,room_name,dev_name,func_command):
        """
        :param func_command: 0:"off",1:"on"
        :return:
        """
        # func_command={
        #     0:"off",
        #     1:"on",
        # }
        dev_class_type="light"
        self.__send_msg(dev_class_type,room_name,dev_name,func_command)

    def fresh_air_system_c(self,room_name,dev_name,func_command):
        """
        :param func_command: 0:"off",1:"on",2:"wind_speed_low",3:"wind_speed_middle",4:"wind_speed_height"
        :return:
        """
        # func_command={
        #     0:"off",
        #     1:"on",
        #     2:"wind_speed_low",
        #     3:"wind_speed_middle",
        #     4:"wind_speed_height"
        # }
        dev_class_type="fresh_air_system"
        self.__send_msg(dev_class_type,room_name,dev_name,func_command)

    def curtain_c(self,room_name,dev_name,func_command):
        """
        :param func_command: 0:"close",1:"open",2:"stop"
        :return:
        """
        # func_command={
        #     0:"close",
        #     1:"open",
        #     2:"stop"
        # }
        dev_class_type="curtain"
        self.__send_msg(dev_class_type,room_name,dev_name,func_command)

    def dimmer_c(self,room_name,dev_name,func_command,value=0):
        """
        :param func_command: 0:"off",1:"on",2:"brightness"
        :param value:1-100
        :return:
        """
        # func_command={
        #     0:"off",
        #     1:"on",
        #     2:"brightness"
        # }
        func_value={"value":0}
        if func_command=="brightness":
            if value<=0:
                func_value={"brightness":1}
            elif value>100:
                func_value={"brightness":100}
            else:
                func_value={"brightness":value}

        dev_class_type="dimmer"
        self.__send_msg(dev_class_type,room_name,dev_name,func_command,func_value=func_value)

    def smartlock_c(self,room_name,dev_name,func_command,password):
        password=self.__md5(password)
        self.smart_lock_apply_c("smartlock",room_name,dev_name,func_command,password)

    def smartlock_hl_c(self,room_name,dev_name,func_command,password):
        password=self.__md5(password)
        self.smart_lock_apply_c("smartlock_hl",room_name,dev_name,func_command,password)

    def smartlock_at_c(self,room_name,dev_name,func_command,password):
        password=self.__md5(password)
        self.smart_lock_apply_c("smartlock_at",room_name,dev_name,func_command,password)

    def smart_lock_apply_c(self,dev_class_type,room_name,dev_name,func_command,password):
        """
        :param func_command: 0:"open_lock"
        :return:
        """
        # func_command={
        #     0:"open_lock"
        # }
        params={
            "password":password
        }
        func_value=0
        dev_class_type=dev_class_type
        self.__send_msg(dev_class_type,room_name,dev_name,func_command,func_value=func_value,extend_params=params)

    def air_condition_c(self,room_name,dev_name,func_command,value=0):
        self.air_condition_apply_c("aircondition",room_name,dev_name,func_command,value=value)

    def icool_c(self,room_name,dev_name,func_command,value=0):
        self.air_condition_apply_c("icool",room_name,dev_name,func_command,value=value)

    def air_condition_apply_c(self,dev_class_type,room_name,dev_name,func_command,value=0):
        """
        :param func_command: 0:"off",1:"on",....
        :return:
        """
        # func_command={
        #     0:"off",
        #     1:"on",
        #     2:"temperature",
        #     3:"mode_cool",
        #     4:"mode_hot",
        #     5:"mode_wet",
        #     6:"mode_wind",
        #     7:"mode_auto",
        #     8:"wind_speed_height",
        #     9:"wind_speed_middle",
        #     10:"wind_speed_low",
        #     11:"wind_speed_auto",
        #     12:"wind_direction_horizontal",
        #     13:"wind_direction_vertical",
        #     14:"wind_direction_hand",
        #     15:"sleep_on",
        #     16:"sleep_off",
        #     17:"heat_on",
        #     18:"heat_off",
        #     19:"strong_on",
        #     20:"strong_off",
        #     21:"light_on",
        #     22:"light_off",
        #     23:"airclear_on",
        #     24:"airclear_off",
        #     25:"economic_on",
        #     26:"economic_off"
        # }
        func_value={"value":0}
        if func_command=="temperature":
            if value<16:
                value=16
            elif value>32:
                value=32
            func_value={"value":value}

        dev_class_type=dev_class_type
        self.__send_msg(dev_class_type,room_name,dev_name,func_command,func_value=func_value)

    def tv_c(self,room_name,dev_name,func_command,value=0):
        """
        :param func_command: 0:"on_off",....
        :return:
        """
        # func_command={
        #     0:"on_off",
        #     1:"mute",
        #     2:"channal+",
        #     3:"channal-",
        #     4:"volume+",
        #     5:"volume-",
        #     6:"up",
        #     7:"down",
        #     8:"left",
        #     9:"right",
        #     10:"ok",
        #     11:"back",
        #     12:"key_0",
        #     13:"key_1",
        #     14:"key_2",
        #     15:"key_3",
        #     16:"key_4",
        #     17:"key_5",
        #     18:"key_6",
        #     19:"key_7",
        #     20:"key_8",
        #     21:"key_9",
        #     22:"menu",
        #     23:"at_tv",
        #     24:"pingxian",
        #     25:"wangfan",
        #     26:"zhishi",
        #     27:"normal",
        #     28:"liyin",
        #     29:"picinpic",
        #     30:"sleep",
        #     31:"sound",
        #     32:"switch",
        #     33:"proportion",
        #     34:"channel"
        # }
        func_value={"value":0}
        if func_command=="channel":
            func_value={"channel_num":value}
        dev_class_type="tv"
        self.__send_msg(dev_class_type,room_name,dev_name,func_command,func_value=func_value)

    def dvb_c(self,room_name,dev_name,func_command,value=0):
        """
        :param func_command: 0:"on_off",....
        :return:
        """
        # func_command={
        #     0:"on_off",
        #     1:"mute",
        #     2:"channal+",
        #     3:"channal-",
        #     4:"volume+",
        #     5:"volume-",
        #     6:"up",
        #     7:"down",
        #     8:"left",
        #     9:"right",
        #     10:"ok",
        #     11:"back",
        #     12:"key_0",
        #     13:"key_1",
        #     14:"key_2",
        #     15:"key_3",
        #     16:"key_4",
        #     17:"key_5",
        #     18:"key_6",
        #     19:"key_7",
        #     20:"key_8",
        #     21:"key_9",
        #     22:"menu",
        #     23:"playbill",
        #     24:"audioch",
        #     25:"exit",
        #     26:"pageup",
        #     27:"pagedn",
        #     28:"zixun",
        #     29:"favor",
        #     30:"info",
        #     31:"red",
        #     32:"green",
        #     33:"yellow",
        #     34:"blue",
        #     35:"channel"
        # }
        func_value={"value":0}
        if func_command=="channel":
            func_value={"channel_num":value}
        dev_class_type="dvb"
        self.__send_msg(dev_class_type,room_name,dev_name,func_command,func_value=func_value)

    def dvd_c(self,room_name,dev_name,func_command):
        """
        :param func_command: 0:"on_off",....
        :return:
        """
        # func_command={
        #     0:"on_off",
        #     1:"play",
        #     2:"pause",
        #     3:"stop",
        #     4:"play_next",
        #     5:"play_previous",
        #     6:"volume+",
        #     7:"volume-",
        #     8:"warehouse_in_out"
        # }
        dev_class_type="dvd"
        self.__send_msg(dev_class_type,room_name,dev_name,func_command)

    def amplifier_c(self,room_name,dev_name,func_command):
        """
        :param func_command: 0:"on_off",....
        :return:
        """
        # func_command={
        #     0:"on_off",
        #     1:"source_tv",
        #     2:"source_dvd",
        #     3:"volume+",
        #     4:"volume-",
        #     5:"audioch_left",
        #     6:"audioch_right"
        # }
        dev_class_type="amplifier"
        self.__send_msg(dev_class_type,room_name,dev_name,func_command)

    def rgb_light_c(self,room_name,dev_name,func_command,brightness=1,r=0,g=0,b=0,rgb_mode="colour",speed=1):
        """
        :param func_command: 0:"off",1:"on",2:"brightness"
        :param value:1-100
        :return:
        """
        # func_command={
        #     0:"off",
        #     1:"on",
        #     2:"brightness",
        #     3:"rgb_toning",
        #     4:"rgb_mode",
        #     5:"rgb_toning_brightness"
        # }
        func_value={"value":0}

        if brightness<=0:
            brightness=1
        elif brightness>100:
            brightness=100

        if r<0:
            r=0
        elif r>255:
            r=255
        if g<0:
            g=0
        elif g>255:
            g=255
        if b<0:
            b=0
        elif b>255:
            b=255

        if rgb_mode<0:
            rgb_mode=1
        elif rgb_mode>8:
            rgb_mode=8
        if speed<0:
            speed=1
        elif speed>100:
            speed=100

        if func_command=="brightness":
            func_v={"brightness":brightness}
            func_value.update(func_v)

        elif func_command=="rgb_toning":
            func_v={"r":r,"g":g,"b":b}
            func_value.update(func_v)

        elif func_command=="rgb_mode":
            # rgb_mode_dict={
            #     1:"red",
            #     2:"orange",
            #     3:"yellow",
            #     4:"green",
            #     5:"cyan",
            #     6:"blue",
            #     7:"purple",
            #     8:"colour"
            # }
            func_v={"rgb_mode":rgb_mode,"speed":speed}
            func_value.update(func_v)

        elif func_command=="rgb_toning_brightness":
            func_v={"r":r,"g":g,"b":b,"brightness":brightness}
            func_value.update(func_v)

        dev_class_type="rgb_light"
        self.__send_msg(dev_class_type,room_name,dev_name,func_command,func_value=func_value)

    def dryingracks_c(self,room_name,dev_name,func_command,value=0):
        """
        :param func_command: 0:"on_off",....
        :return:
        """
        # func_command={
        #     0:"rise",
        #     1:"fall",
        #     2:"stop",
        #     3:"dis_on",
        #     4:"dis_off",
        #     5:"bakedry_on",
        #     6:"bakedry_off",
        #     7:"winddry_on",
        #     8:"winddry_off",
        #     9:"light_on",
        #     10:"light_off"
        # }
        func_value={"voice":"voice_on","dis":"dis_off","bakedry":"bakedry_on","winddry":"winddry_on",
                    "light":"light_on","anion":"anion_on","position":"other","motor":"stop",
                    "bakedryt":180,
                    "winddryt":180,
                    "dist":30}
        if func_command=="dis_on":
            func_value={"voice":"voice_on","dis":"dis_off","bakedry":"bakedry_on","winddry":"winddry_on",
                    "light":"light_on","anion":"anion_on","position":"other","motor":"stop",
                    "bakedryt":180,
                    "winddryt":180,
                    "dist":value}
        elif func_command=="bakedry_on":
            func_value={"voice":"voice_on","dis":"dis_off","bakedry":"bakedry_on","winddry":"winddry_on",
                "light":"light_on","anion":"anion_on","position":"other","motor":"stop",
                "bakedryt":value,
                "winddryt":180,
                "dist":30}
        elif func_command=="winddry_on":
            func_value={"voice":"voice_on","dis":"dis_off","bakedry":"bakedry_on","winddry":"winddry_on",
                "light":"light_on","anion":"anion_on","position":"other","motor":"stop",
                "bakedryt":180,
                "winddryt":value,
                "dist":30}

        dev_class_type="dryingracks"
        self.__send_msg(dev_class_type,room_name,dev_name,func_command,func_value=func_value)

    def coordin_at_speaker_c(self,room_name,dev_name,func_command,volume=1,play_mode="single_loop"):
        self.coordin_at_speaker_apply_c("coordin_at_speaker",room_name,dev_name,func_command,volume=volume,play_mode=play_mode)

    def coordin_xz_speaker_c(self,room_name,dev_name,func_command):
        self.coordin_at_speaker_apply_c("coordin_xz_speaker",room_name,dev_name,func_command)

    def coordin_bsp_speaker_c(self,room_name,dev_name,func_command,volume=1,play_mode="single_loop",audio_src="network"):
        self.coordin_at_speaker_apply_c("speaker_panel",room_name,dev_name,func_command,volume=volume,play_mode=play_mode,audio_src=audio_src)


    def coordin_at_speaker_apply_c(self,dev_class_type,room_name,dev_name,func_command,volume=1,play_mode="single_loop",audio_src="network"):
        """
        :param func_command: 0:"on_off",....
        :return:
        """
        # func_command={
        #     0:"play",
        #     1:"pause",
        #     2:"mute_on",
        #     3:"mute_off",
        #     4:"play_next",
        #     5:"play_previous",
        #     6:"volume+",
        #     7:"volume-",
        #     8:"volume",
        #     9:"play_mode",
        #     10:"audio_src"
        # }
        func_value={"value":0}
        if func_command=="volume":
            if volume<=0:
                volume=1
            elif volume>15:
                volume=15
            func_value={"volume":volume}
        elif func_command=="play_mode":
            # play_mode_all={
            #     0:"single_loop",
            #     1:"sort_play",
            #     2:"sort_loop",
            #     3:"random"
            # }
            func_value={"play_mode":play_mode}
        elif func_command=="audio_src":
            # audio_src_all={
            #     0:"network",
            #     1:"bluetooth",
            #     2:"radio",
            #     3:"mp3",
            #     4:"dvd"
            # }
            func_value={"play_mode":audio_src}

        dev_class_type=dev_class_type
        self.__send_msg(dev_class_type,room_name,dev_name,func_command,func_value=func_value)


    def __send_msg(self,dev_class_type,room_name,dev_name,func_command,func_value={"value":0},extend_params=None):
        if user.get_info_dict("Net_flag")==1:
            cmd={
                "device_name":dev_name,
                "room_name":room_name,
                "func_command":func_command,
                "dev_class_type":dev_class_type,
                "func_value":func_value,
                "msg_type":"device_control",
                "command":"control",
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
                "device_name":dev_name,
                "room_name":room_name,
                "func_command":func_command,
                "dev_class_type":dev_class_type,
                "func_value":func_value,
                "msg_type":"device_control",
                "command":"control",
                "from_role":"phone",
                "from_account":user.get_info_dict("USERNAME")
            }
            if extend_params:
                cmd.update(extend_params)
            self.send_all(cmd,flag="dynamic")

    def scene_c(self,control_name,password=""):
        cmd={
            "control_name":control_name,
            "password":password,
            "msg_type":"combination_control_manager",
            "command":"start",
            "from_role":"phone",
            "from_account":user.get_info_dict("USERNAME")
        }
        if user.get_info_dict("Net_flag")==1:
            sendmsg=self.__sendmsgformat(cmd)
            # print(sendmsg)
            res_msg=self._request("post",msg=sendmsg)
            # print(res_msg)
        elif user.get_info_dict("Net_flag")==0:
            self.send_all(cmd,flag="dynamic")

    def security_mode_c(self,security_mode,password=""):
        """
        :param security_mode_num: 0:"home",1:"out",2:"sleep",3:"disarm"
        :param password:
        :return:
        """
        # security_mode={
        #     0:"home",
        #     1:"out",
        #     2:"sleep",
        #     3:"disarm"
        # }
        cmd={
            "security_mode":security_mode,
            "password":password,
            "msg_type":"security_mode_change",
            "command":"modify",
            "from_role":"phone",
            "from_account":user.get_info_dict("USERNAME")
        }
        if user.get_info_dict("Net_flag")==1:
            sendmsg=self.__sendmsgformat(cmd)
            # print(sendmsg)
            res_msg=self._request("post",msg=sendmsg)
            # print(res_msg)
        elif user.get_info_dict("Net_flag")==0:
            self.send_all(cmd,flag="dynamic")


    def monitor_c(self,room_name,dev_name):
        cmd={
            "device_name":dev_name,
            "room_name":room_name,
            "msg_type":"camera_monitor_manager",
            "command":"monitor",
            "from_role":"phone",
            "from_account":user.get_info_dict("USERNAME")
        }
        if user.get_info_dict("Net_flag")==1:
            sendmsg=self.__sendmsgformat(cmd)
            # print(sendmsg)
            self._request("post",msg=sendmsg)
            # print(res_msg)
        elif user.get_info_dict("Net_flag")==0:
            self.send_all(cmd,flag="dynamic")



    def __sendmsgformat(self,msg=None):
        sendmsg={
            "cmd":"send_msg",
            "to_username":user.get_info_dict("SIPADDRS"),
            "msg":json.dumps(msg),
            "subject":"control"
             }
        return sendmsg

    def __md5(self,str):
        """
        九宫格排列：
        0 1 2
        3 4 5
        6 7 8
        :param str:
        :return:
        """
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

